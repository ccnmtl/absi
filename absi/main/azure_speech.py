import boto3
import json
import os
import subprocess  # nosec
import tempfile
from pathlib import Path
from django.conf import settings
import azure.cognitiveservices.speech as speechsdk


s3 = boto3.client('s3', region_name=settings.AWS_REGION)


def download_and_transcode_s3_audio(bucket: str, key: str) -> str:
    suffix = Path(key).suffix or '.webm'

    with tempfile.NamedTemporaryFile(
        suffix=suffix,
        delete=False,
    ) as input_file:
        input_path = input_file.name

    with tempfile.NamedTemporaryFile(
        suffix='.wav',
        delete=False,
    ) as output_file:
        output_path = output_file.name

    try:
        s3.download_file(bucket, key, input_path)

        # Transcode recorded audio to PCM, for Azure.
        completed_process = subprocess.run([  # nosec
            'ffmpeg', '-y',
            '-i', input_path,
            '-ac', '1',
            '-ar', '16000',
            '-af', 'loudnorm',
            '-c:a', 'pcm_s16le',
            output_path,
        ], check=True, capture_output=True, text=True)
        print(completed_process, output_path)

        return output_path
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)


def submit_audio_to_azure(path: str, transcribe_text: str) -> dict | None:
    speech_config = speechsdk.SpeechConfig(
        subscription=settings.AZURE_SPEECH_KEY,
        region=settings.AZURE_SPEECH_REGION,
        speech_recognition_language=settings.ABSI_LANG,
    )

    audio_config = speechsdk.AudioConfig(filename=path)
    recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config,
        audio_config=audio_config,
        language=settings.ABSI_LANG,
    )

    pronunciation_config = speechsdk.PronunciationAssessmentConfig(
        reference_text=transcribe_text,
        grading_system=(
            speechsdk.PronunciationAssessmentGradingSystem.HundredMark,
        ),
        granularity=speechsdk.PronunciationAssessmentGranularity.Word,
        enable_miscue=True,
    )

    # Skip this for now - low support in arabic.
    # pronunciation_config.enable_prosody_assessment()

    pronunciation_config.apply_to(recognizer)

    speech_recognition_result = recognizer.recognize_once()
    print('speech_recognition_result', speech_recognition_result)

    if speech_recognition_result.reason == \
       speechsdk.ResultReason.RecognizedSpeech:
        assessment = speechsdk.PronunciationAssessmentResult(
            speech_recognition_result)
        print('assessment', assessment)

        assessment_json = speech_recognition_result.properties.get(
            speechsdk.PropertyId.SpeechServiceResponse_JsonResult)
        print('assessment_json', assessment_json)

        return json.loads(assessment_json)
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        return {'status': 'no_match'}
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        details = speech_recognition_result.cancellation_details
        raise RuntimeError(
            f'Canceled: {details.reason} {details.error_details}')

    return None
