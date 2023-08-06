import logging
from optparse import make_option

from django.core.management import BaseCommand
from evernote.edam.notestore.ttypes import SyncChunkFilter

from yx.djangohelper import update_or_create
from yx.models import YUser, YNotebook
from yx.utils import cache_note

MAX_ENTITIES = 2 ** 10
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--username'),
        make_option('--fullsync', action='store_true'),
        make_option('--tags', action='store_true'),
        make_option('--notes', action='store_true'),
    )

    def handle(self, username, fullsync, tags, notes, *args, **options):
        logger.debug('username=%s fullsync=%s args=%s, options=%s', username, fullsync, args, options)

        account = YUser.objects.get(username=username)
        devtoken = account.token
        logger.debug('devtoken=%s', devtoken)
        client = account.get_client()
        if fullsync:
            next_usn = 0
        else:
            next_usn = account.last_usn

        # update user profile from yinxiang
        user_store = client.get_user_store()
        user = user_store.getUser(devtoken)
        account.userid_in_evernote = user.id
        account.shardid = user.shardId
        account.save()
        note_store = client.get_note_store()
        fltr = SyncChunkFilter()
        fltr.includeNotes = True
        fltr.includeTags = True
        fltr.includeNoteAttributes = True
        fltr.includeNoteResources = False

        while 1:
            sync_chunk = note_store.getFilteredSyncChunk(devtoken, next_usn, MAX_ENTITIES, fltr)
            if next_usn >= sync_chunk.updateCount:
                break

            logger.debug('chunk usn from %d->%d ==> updateCount=%s,', next_usn, sync_chunk.chunkHighUSN, sync_chunk.updateCount)

            # process sync chunk
            for tag in (sync_chunk.tags or []):
                logging.debug('tag=%s', tag.name.decode('utf-8'))
                yxtag, created = update_or_create(account.tags, guid=tag.guid, defaults=dict(name=tag.name.decode('utf-8')))

            for note in (sync_chunk.notes or []):
                logger.debug('note title=%s', note.title.decode('utf-8'))
                cache_note(account, note)

            for notebook in (sync_chunk.notebooks or []):
                YNotebook.objects.get_or_create(guid=notebook.guid, default=dict(
                    yxaccount=account,
                    name=notebook.name
                ))

            next_usn = sync_chunk.chunkHighUSN

        account.last_usn = next_usn  # sync_chunk.chunkHighUSN
        account.save()
        logger.info('sync completed')
