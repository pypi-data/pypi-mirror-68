from django.conf import settings
from evernote.api.client import EvernoteClient


def get_anonymous_client():
    client = EvernoteClient(consumer_key=settings.EVERNOTE_CONSUMER_KEY,
                            consumer_secret=settings.EVERNOTE_CONSUMER_SECRET,
                            service_host=settings.EVERNOTE_SERVICE_HOST)
    return client
