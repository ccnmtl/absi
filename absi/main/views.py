import boto3
import uuid
from urllib.parse import urlparse
from celery import chain
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.authtoken.models import Token
from s3sign.views import SignS3View
from s3sign.utils import s3_config

from absi.main.tasks import (
    start_transcribe_job, poll_transcription, fetch_transcript,

    start_azure_transcribe_job, poll_azure_transcription,
    fetch_azure_transcript
)


def enqueue_transcription(job_name: str, media_uri: str):
    chain(
        start_transcribe_job.s(job_name, media_uri),
        poll_transcription.s(),
        fetch_transcript.s(),
    ).apply_async()


def enqueue_azure_transcription(job_name: str, media_uri: str):
    chain(
        start_azure_transcribe_job.s(job_name, media_uri),
        poll_azure_transcription.s(),
        fetch_azure_transcript.s(),
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

        s3_uri = request.data['s3_uri']
        url = urlparse(s3_uri)
        s3_path = url.path
        s3_path = s3_path.lstrip('/')
        print(s3_path)

        job_name = 'absi-azure-transcribe-' + str(uuid.uuid4())

        enqueue_azure_transcription(s3_uri, job_name)

        return Response(
            {
                'job_id': None,
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
