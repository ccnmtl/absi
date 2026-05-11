# absi
Arabic Learning R&amp;D

## Requirements                                                                                                                                                                               
This project relies on the following technologies:                                                                                                                                            
* Django
* [django-channels](https://channels.readthedocs.io/en/latest/) - for
  providing live feedback to events via websockets
  * django-channels is using Redis via [channels_redis](https://github.com/django/channels_redis/)
* [celery](https://docs.celeryq.dev/en/stable/index.html) - for defining async tasks in Django
  * Currently using Amazon SQS as queueing back-end (broker), but any
    other back-end such as RabbitMQ can work as well.

Audio services:
* [Amazon Polly](https://aws.amazon.com/polly/) - provides text-to-speech synthesis
  * [Python SDK Docs](https://docs.aws.amazon.com/boto3/latest/reference/services/polly.html)
* [Amazon Transcribe](https://aws.amazon.com/transcribe/) - provides
  speech transcription. At least in Arabic, accuracy is
  questionable. Not sure if this will be useful or not.
  * [Python SDK Docs](https://docs.aws.amazon.com/code-library/latest/ug/python_3_transcribe_code_examples.html)
* Azure Speech - provides speech analysis / transcription / assessment
  * [Python SDK Docs](https://learn.microsoft.com/en-us/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech?view=azure-python)