import logging
import time

from django.conf import settings
from django.contrib.auth.models import AbstractUser, User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from evernote.api.client import EvernoteClient

INAPPLINKFORMAT = 'evernote:///view/{userId}/{shardId}/{noteGuid}/{noteGuid}/'
HTTPLINKFORMAT = 'https://{service}/shard/{shardId}/nl/{userId}/{noteGuid}/'
NOTE_THUMBNAIL_URL_FORMAT = 'https://{host}/shard/{shardId}/thm/note/{GUID}'

logger = logging.getLogger(__name__)


def _nanoseconds_now():
    return int(time.time() * 1000)


class YUserManager(models.Manager):

    def get_anonymous_client(self):
        client = EvernoteClient(consumer_key=settings.EVERNOTE_CONSUMER_KEY,
                                consumer_secret=settings.EVERNOTE_CONSUMER_SECRET,
                                service_host=settings.EVERNOTE_SERVICE_HOST)
        return client


class YUser(models.Model):
    user = models.OneToOneField(User, related_name='+', on_delete=models.CASCADE)

    username = models.CharField(max_length=32)
    token = models.TextField(null=True, blank=True)
    userid_in_evernote = models.IntegerField(default=0)
    shardid = models.CharField(max_length=10, default='s0')
    last_usn = models.IntegerField(default=0)

    objects = YUserManager()

    def __unicode__(self):
        return '%s@%s' % (self.username, settings.EVERNOTE_SERVICE_HOST)

    def get_client(self):
        # type: () -> EvernoteClient
        client = EvernoteClient(token=self.token,
                                service_host=settings.EVERNOTE_SERVICE_HOST)

        return client


class YTag(models.Model):
    yxaccount = models.ForeignKey('YUser', related_name='tags')
    notes = models.ManyToManyField('YNote', related_name='tags')
    guid = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class YNotebook(models.Model):
    yxaccount = models.ForeignKey('YUser', related_name='notebooks')
    name = models.CharField(max_length=100)
    guid = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class YNote(models.Model):
    yxaccount = models.ForeignKey('YUser', related_name='notes', on_delete=models.PROTECT)
    guid = models.CharField(max_length=100, unique=True)
    notebook = models.ForeignKey('YNotebook', related_name='notes')
    title = models.CharField(max_length=1000)
    created = models.BigIntegerField(default=_nanoseconds_now)
    updated = models.BigIntegerField(default=_nanoseconds_now)
    content = models.TextField(null=True, blank=True)
    content_length = models.IntegerField(default=0)
    attributes = models.TextField(default='', blank=True)
    reminder_time = models.BigIntegerField(blank=True, null=True)
    reminder_done_time = models.BigIntegerField(blank=True, null=True)

    usn = models.IntegerField(default=0)

    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        if self.deleted:
            return '<strike>%s</strike>' % self.title

        return self.title

    def tagged(self, *tagnames):
        try:
            return self.tags.filter(name__in=tagnames).count() == len(tagnames)
        except ObjectDoesNotExist:
            pass

    @property
    def link_in_app(self):
        return INAPPLINKFORMAT.format(userId=self.yxaccount.userid_in_evernote,
                                      shardId=self.yxaccount.shardid,
                                      noteGuid=self.guid)

    class Meta:
        ordering = ('-updated',)
