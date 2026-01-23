import uuid
from celery import chain
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.authtoken.models import Token

from absi.main.tasks import (
    start_transcribe_job, poll_transcription, fetch_transcript
)


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


class QueueTranscribeJobView(APIView):
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
