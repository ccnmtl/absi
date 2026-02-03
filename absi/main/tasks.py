import boto3
import requests
from celery import shared_task
from django.conf import settings
from absi.main.websockets import notify_ws


transcribe = boto3.client(
    'transcribe',
    region_name=settings.AWS_REGION
)


@shared_task
def start_transcribe_job(s3_uri: str, job_name: str) -> str:
    print('queue_transcribe_job', s3_uri)
    # TODO: limit audio length before starting job.

    print('queueing job', job_name)
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        LanguageCode='en-US',
        Media={
            'MediaFileUri': s3_uri,
        },
    )

    notify_ws('Transcript loading...')
    return job_name


@shared_task(
    bind=True,
    max_retries=60,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=60,
    retry_jitter=True
)
def poll_transcription(self, job_name):
    print('poll_transcription', job_name)
    response = transcribe.get_transcription_job(
        TranscriptionJobName=job_name
    )

    job = response['TranscriptionJob']
    status = job['TranscriptionJobStatus']

    if status == 'COMPLETED':
        return job['Transcript']['TranscriptFileUri']
    if status == 'FAILED':
        raise RuntimeError(job['FailureReason'])

    raise Exception('Job still in progress')


@shared_task
def fetch_transcript(transcript_uri):
    print('fetch_transcript', transcript_uri)
    response = requests.get(transcript_uri, timeout=30)
    response.raise_for_status()
    data = response.json()
    transcript_text = data['results']['transcripts'][0]['transcript']

    print('transcript_text', transcript_text)
    notify_ws(transcript_text)
    return transcript_text
