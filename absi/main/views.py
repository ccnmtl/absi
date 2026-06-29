import boto3
import uuid
from celery import chain
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from pagetree.generic.views import PageView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.authtoken.models import Token
from s3sign.views import SignS3View
from s3sign.utils import s3_config
import unicodedata
from urllib.parse import urlparse

from absi.main.tasks import (
    start_transcribe_job, poll_transcription, fetch_transcript,

    start_azure_transcribe_job
)
from absi.main.models import PlayBlock


MAX_LENGTH = 512


def enqueue_transcription(job_name: str, media_uri: str):
    chain(
        start_transcribe_job.s(job_name, media_uri),
        poll_transcription.s(),
        fetch_transcript.s(),
    ).apply_async()


class IndexView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'main/index.html'


class LoginSplashView(TemplateView):
    template_name = 'main/login_splash.html'


class TranscribeView(LoginRequiredMixin, TemplateView):
    template_name = 'main/transcribe.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request and self.request.user:
            token, _ = Token.objects.get_or_create(user=self.request.user)
            context['token'] = token

        return context


class PollyAudioView(LoginRequiredMixin, View):
    audio_formats = {
        'ogg': {
            'output_format': 'ogg_vorbis',
            'extension': 'ogg',
            'content_type': 'audio/ogg',
        },
        'mp3': {
            'output_format': 'mp3',
            'extension': 'mp3',
            'content_type': 'audio/mpeg',
        }
    }

    # 'text' or 'ssml', for Polly's TextType.
    text_type = 'text'

    """
    Apply phoneme overrides for certain words which need it.
    """
    def apply_phoneme_overrides(self, text: str) -> str:
        normalized = unicodedata.normalize('NFC', text.strip())
        if normalized == unicodedata.normalize('NFC', 'أَمُرٌّ'):
            self.text_type = 'ssml'
            text = """
            <speak>
                <phoneme alphabet="ipa" ph="ʔamurrun">أَمُرٌّ</phoneme>
            </speak>
            """
        elif normalized == unicodedata.normalize('NFC', 'وَلودٌ'):
            self.text_type = 'ssml'
            text = """
            <speak>
                <phoneme alphabet="ipa" ph="waluːdun">وَلودٌ</phoneme>
            </speak>
            """

        return text

    def get(self, request, *args, **kwargs):
        polly_client = boto3.Session(
            region_name=settings.AWS_REGION,
        ).client('polly')

        text = request.GET.get('text', None)

        if not text:
            pageblock_id = kwargs.get('pk', '')
            pageblock = None
            if pageblock_id:
                pageblock = get_object_or_404(PlayBlock, pk=pageblock_id)

            text = None
            if pageblock:
                text = pageblock.text

        if not text:
            return JsonResponse({'error': 'Text is required'}, status=400)

        if len(text) > MAX_LENGTH:
            return JsonResponse({
                'error':
                f'Text too long. Max length is {MAX_LENGTH} characters.'
            }, status=400)

        text = self.apply_phoneme_overrides(text)

        voice_param = request.GET.get('voice', '')
        audio_format_param = request.GET.get('audio_format', '')

        voice_id = 'Hala'
        if voice_param == 'Zayd':
            voice_id = 'Zayd'

        audio_format = PollyAudioView.audio_formats.get('ogg')
        if audio_format_param == 'mp3':
            audio_format = PollyAudioView.audio_formats.get('mp3')

        response = polly_client.synthesize_speech(
            VoiceId=voice_id,
            OutputFormat=audio_format.get('output_format'),
            SampleRate='44100',
            Text=text,
            TextType=self.text_type,
            Engine='neural')

        audio_stream = response['AudioStream'].read()
        return HttpResponse(
            audio_stream,
            content_type=audio_format.get('content_type'),
            headers={
                'Content-Disposition':
                'inline; filename=speech.{}'.format(
                    audio_format.get('extension'))
            })


class AuthedPageView(LoginRequiredMixin, PageView):
    def get_extra_context(self):
        context = super().get_extra_context()

        if self.request and self.request.user:
            token, _ = Token.objects.get_or_create(user=self.request.user)
            context['token'] = token

        return context


class QueueAWSTranscribeJobView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print('transcribe post')

        s3_uri = request.data['s3_uri']
        job_name = 'absi-transcribe-' + str(uuid.uuid4())
        enqueue_transcription(s3_uri, job_name)

        return Response(
            {
                'job_id': None,
                'status': 'QUEUED',
            },
            status=status.HTTP_202_ACCEPTED,
        )


class AzureTranscribeJobView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print('azure transcribe post')

        s3_uri = request.data.get('s3_uri')
        transcribe_text = request.data.get('transcribe_text')
        url = urlparse(s3_uri)
        s3_path = url.path
        s3_path = s3_path.lstrip('/')
        print(s3_path)

        task = start_azure_transcribe_job.delay(s3_path, transcribe_text)
        print('AzureTranscribeJobView task', task)

        return Response(
            {
                'task_id': task.id,
                'status': 'QUEUED',
            },
            status=status.HTTP_202_ACCEPTED,
        )


class SignS3ECSView(SignS3View):
    """
    SignS3View that doesn't use access keys. This is how we auth on
    ECS using task roles.
    """
    def get_aws_access_key(self):
        return None

    def get_aws_secret_key(self):
        return None

    def dispatch(self, request, *args, **kwargs):
        if not getattr(self, 's3_client', None):
            self.s3_client = boto3.client(
                's3', config=s3_config,
                region_name=self.aws_region_name,
            )

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        if not getattr(self, 's3_client', None):
            self.s3_client = boto3.client(
                's3', config=s3_config,
                region_name=self.aws_region_name,
            )

        return super().get(request)
