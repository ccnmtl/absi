import boto3
import os
import subprocess  # nosec
import tempfile
from pathlib import Path
from django.conf import settings
import azure.cognitiveservices.speech as speechsdk


s3 = boto3.client('s3', region_name=settings.AWS_REGION)


def transcribe_audio_file(path: str) -> str:
    speech_config = speechsdk.SpeechConfig(
        subscription=settings.AZURE_SPEECH_KEY,
        region=settings.AZURE_SPEECH_REGION,
        speech_recognition_language='en-US',
    )

    audio_config = speechsdk.AudioConfig(filename=path)
    recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config,
        audio_config=audio_config,
    )

    result = recognizer.recognize_once()
    print('result', result)

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text

    if result.reason == speechsdk.ResultReason.NoMatch:
        raise RuntimeError('No speech recognized')

    if result.reason == speechsdk.ResultReason.Canceled:
        details = result.cancellation_details
        raise RuntimeError(
            f'Canceled: {details.reason} {details.error_details}')


def download_and_transcribe_s3_audio(bucket: str, key: str) -> str:
    suffix = '.webm'
    file_path = Path(key)
    if file_path and file_path.suffix:
        suffix = file_path.suffix

    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
        tmp_path = f.name
        tmp_stem = Path(tmp_path).stem

    s3.download_file(bucket, key, tmp_path)

    # Transcode recorded audio to PCM, for Azure.
    completed_process = subprocess.run([  # nosec
        'ffmpeg', '-y',
        '-i', tmp_path,
        '-ac', '1',
        '-ar', '16000',
        '-af', 'loudnorm',
        '-c:a', 'pcm_s16le',
        f'/tmp/{tmp_stem}.wav'  # nosec
    ], check=True)
    print(completed_process)

    try:
        return transcribe_audio_file(f'/tmp/{tmp_stem}.wav')  # nosec
    finally:
        os.remove(tmp_path)
        os.remove(f'/tmp/{tmp_stem}.wav')  # nosec
