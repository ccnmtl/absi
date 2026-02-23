import os
import boto3
import requests
from celery import shared_task
from django.conf import settings
from absi.main.websockets import notify_ws
from absi.main.azure_speech import (
    submit_audio_to_azure, download_and_transcode_s3_audio
)


boto_transcribe = boto3.client(
    'transcribe',
    region_name=settings.AWS_REGION
)


@shared_task
def start_transcribe_job(s3_uri: str, job_name: str) -> str:
    print('queue_transcribe_job', s3_uri)
    # TODO: limit audio length before starting job.

    print('queueing job', job_name)
    boto_transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        LanguageCode=settings.ABSI_LANG,
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
    response = boto_transcribe.get_transcription_job(
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


@shared_task
def start_azure_transcribe_job(s3_path: str, job_name: str) -> str:
    print('queue_azure_transcribe_job', s3_path)
    # TODO: limit audio length before starting job.

    wav_filepath = download_and_transcode_s3_audio(
        settings.AWS_UPLOAD_BUCKET, s3_path)
    print('result', wav_filepath)
    poll_url = submit_audio_to_azure(wav_filepath)
    print('poll_url', poll_url)
    os.remove(wav_filepath)

    notify_ws('Transcript loading...')
    return poll_url


@shared_task(
    bind=True,
    max_retries=60,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=60,
    retry_jitter=True
)
def poll_azure_transcription(self, job_name):
    print('poll_transcription', job_name)
    response = boto_transcribe.get_transcription_job(
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
def fetch_azure_transcript(transcript_uri):
    print('fetch_transcript', transcript_uri)
    response = requests.get(transcript_uri, timeout=30)
    response.raise_for_status()
    data = response.json()
    transcript_text = data['results']['transcripts'][0]['transcript']

    print('transcript_text', transcript_text)
    notify_ws(transcript_text)
    return transcript_text
