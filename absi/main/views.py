import boto3
import uuid
from urllib.parse import urlparse
from celery import chain
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from pagetree.generic.views import PageView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.authtoken.models import Token
from s3sign.views import SignS3View
from s3sign.utils import s3_config

from absi.main.tasks import (
    start_transcribe_job, poll_transcription, fetch_transcript,

    start_azure_transcribe_job
)


MAX_LENGTH = 200


def enqueue_transcription(job_name: str, media_uri: str):
    chain(
        start_transcribe_job.s(job_name, media_uri),
        poll_transcription.s(),
        fetch_transcript.s(),
    ).apply_async()


class IndexView(TemplateView):
    template_name = 'main/index.html'


class TranscribeView(LoginRequiredMixin, TemplateView):
    template_name = 'main/transcribe.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request and self.request.user:
            token, _ = Token.objects.get_or_create(user=self.request.user)
            context['token'] = token

        return context


class PollyAudioView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        polly_client = boto3.Session(
            region_name=settings.AWS_REGION,
        ).client('polly')
        text = kwargs.get('text', '')
        voice = request.GET.get('voice', '')

        if not text:
            return JsonResponse({'error': 'Text is required'}, status=400)

        if len(text) > MAX_LENGTH:
            return JsonResponse({
                'error':
                f'Text too long. Max length is {MAX_LENGTH} characters.'
            }, status=400)

        voice_id = 'Hala'
        if voice == 'Zayd':
            voice_id = 'Zayd'

        response = polly_client.synthesize_speech(
            VoiceId=voice_id,
            OutputFormat='mp3',
            Text=text,
            Engine='neural')

        audio_stream = response['AudioStream'].read()
        return HttpResponse(
            audio_stream,
            content_type='audio/mpeg',
            headers={
                'Content-Disposition': "inline; filename='speech.mp3'"
            })


class AuthedPageView(LoginRequiredMixin, PageView):
    pass


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
