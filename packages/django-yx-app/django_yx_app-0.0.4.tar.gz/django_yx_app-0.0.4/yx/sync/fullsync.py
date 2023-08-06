import logging

from enum import IntEnum
from evernote.edam.notestore.ttypes import SyncChunkFilter

from yx.models import SyncMark, YUser
from yx.sync.exceptions import ConflictError
from yx.sync.notebooks import cache_notebook
from yx.sync.notes import push_note_create, push_note_update, save_note_in_local_db
from yx.sync.tags import pull_a_tag

MAX_ENTITIES = 2 ** 10


class ConflictOption(IntEnum):
    RAISE_EXCEPTION = 0
    FORCE_OVERWRITE = 1


logger = logging.getLogger('yx.sync')


def pull(username, fullsync=None, conflict_option=ConflictOption.FORCE_OVERWRITE, **options):
    # logger.debug('databases=%s', settings.DATABASES)
    logger.debug('username=%s fullsync=%s  options=%s', username, fullsync, options)
    # logger.debug('all=%s', YUser.objects.all())
    account = YUser.objects.get(username=username)
    devtoken = account.token
    client = account.get_client()
    if fullsync:
        next_usn = 0
    else:
        next_usn = account.last_usn

    # pull user info #################################
    user_store = client.get_user_store()
    user = user_store.getUser(devtoken)
    account.userid_in_evernote = user.id
    account.shardid = user.shardId
    account.save()

    # pull chunk #################################
    note_store = client.get_note_store()
    fltr = SyncChunkFilter(
        includeNotebooks=True,
        includeNotes=True,
        includeTags=True,
        includeNoteAttributes=True,
    )
    while 1:
        sync_chunk = note_store.getFilteredSyncChunk(devtoken, next_usn, MAX_ENTITIES, fltr)
        # If updateCount
        # and chunkHighUSN are identical, that means that this is the last chunk
        # in the account ... there is no more recent information.
        if next_usn >= sync_chunk.updateCount:
            break

        logger.debug('------- process (%s,%s) of %s updates', next_usn, sync_chunk.chunkHighUSN, sync_chunk.updateCount)

        # pull tags #################################
        logger.debug('--------- pull tags --------')
        for tag in (sync_chunk.tags or []):
            yxtag = pull_a_tag(account, tag)

        # pull notebooks #################################
        logger.debug('--------- pull notebooks --------')
        for notebook in (sync_chunk.notebooks or []):
            ynb = cache_notebook(notebook, account)

        # pull note info #################################
        logger.debug('--------- pull notes --------')
        for note in (sync_chunk.notes or []):
            logger.debug('note title=%s', note.title.decode('utf-8'))
            ynote = save_note_in_local_db(note, account, conflict_option)

        next_usn = sync_chunk.chunkHighUSN

    account.last_usn = next_usn  # sync_chunk.chunkHighUSN
    account.save()
    logger.info('sync completed')


def push(username, fullsync=None, conflict_option=ConflictOption.RAISE_EXCEPTION, **options):
    account = YUser.objects.get(username=username)
    token = account.token
    lastusn = account.last_usn

    client = account.get_client()
    note_store = client.get_note_store()

    # push tags
    for tag in account.tags.filter(sync_mark=SyncMark.NEW):
        # create tag
        pass

    for tag in account.tags.filter(sync_mark=SyncMark.UPDATE):
        # update tag
        pass

    # push notebooks
    for tag in account.notebooks.filter(sync_mark=SyncMark.NEW):
        # create tag
        pass

    for tag in account.notebooks.filter(sync_mark=SyncMark.UPDATE):
        # update tag
        pass

    # push new notes
    for ynote in account.notes.filter(sync_mark=SyncMark.NEW):
        logger.info('push to create note "%s"', ynote.title)
        push_note_create(ynote, note_store, token)

    for ynote in account.notes.filter(sync_mark=SyncMark.UPDATE):
        logger.info('push to update note "%s"', ynote.title)
        try:
            push_note_update(ynote, note_store, token, conflict_option)
        except ConflictError:
            # todo : mark note conflicted
            logger.warning('note with guid(%s) conflicted', ynote.guid)
            continue


def pullsinglenote(guid, **options):
    account = YUser.objects.get(token=options['token'])
    client = account.get_client()
    note_store = client.get_note_store()

    # note = Yxnote.objects.get(guid=guid)

    # update note content with resource data

    # download resources
    notedata = note_store.getNote(
        account.token, guid,
        True,  # withContent
        False,  # withResourcesData
        False,  # withResourcesRecognition
        False  # withResourcesAlternateData
    )

    save_note_in_local_db(notedata, account, ConflictOption.FORCE_OVERWRITE)

    # todo: download resource, but not now
    # if hasattr(notedata, 'resources') and notedata.resources:
    #     for res in notedata.resources:
    #         logger.debug('res=%s', res)
    #         # update res usn
    #         # write res data into file
    #         fn = binascii.hexlify(res.data.bodyHash)
    #         with open(os.path.join(BASE_DIR, 'files', fn), 'wb') as o:
    #             o.write(res.data.body)

    # convert note content to markdown, and store into db
    # note.save()
