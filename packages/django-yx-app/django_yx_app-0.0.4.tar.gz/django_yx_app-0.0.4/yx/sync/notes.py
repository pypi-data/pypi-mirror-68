import logging

from django.core.exceptions import ObjectDoesNotExist
from evernote.edam.type.ttypes import Note

from yx.djangohelper import update_or_create
from yx.models import SyncMark, YNote, YNotebook, YUser
from .exceptions import ConflictError
from .fullsync import ConflictOption
from .typeconverters import note_from_modelnote, note_to_model_dict

logger = logging.getLogger(__name__)


def save_note_in_local_db(note, yxaccount, conflict_option):
    # type: ( Note, YUser,ConflictOption) -> YNote
    """
    cache note from evernote api into database
    """

    logger.debug('cache_note title=%s', note.title.decode('utf-8'))

    # check usn now
    try:
        ynote = yxaccount.notes.get(guid=note.guid)
        if ynote.usn != note.updateSequenceNum:
            logger.warning('conflict occurred, force overwrite for %s', note.title.decode('utf-8'))

            if conflict_option == ConflictOption.RAISE_EXCEPTION:  # otherwise
                raise ConflictError
            elif conflict_option == ConflictOption.FORCE_OVERWRITE:
                pass

    except ObjectDoesNotExist:
        pass

    notebookGuid = note.notebookGuid
    notebook, created = update_or_create(
        YNotebook.objects,
        guid=notebookGuid,
        defaults=dict(
            yxaccount=yxaccount,
            name=notebookGuid
        )
    )

    d = note_to_model_dict(note)

    # store into db
    ynote, _created = update_or_create(
        yxaccount.notes,
        guid=note.guid,
        defaults=dict(
            notebook=notebook,
            sync_mark=SyncMark.NORMAL,
            **d
        )
    )
    logger.debug('create note(%s) in database', ynote.guid)

    # update note tags
    newtags = []
    for tag_guid in note.tagGuids or []:
        logger.debug('tag_guid=%s', tag_guid)
        tag, _created = update_or_create(
            yxaccount.tags,
            guid=tag_guid,
            defaults=dict(
                name=tag_guid,
                usn=0,
                sync_mark=SyncMark.NORMAL
            )
        )
        newtags.append(tag)
    ynote.tags.clear()
    ynote.tags.add(*newtags)

    return ynote


def push_note_create(ynote, note_store, token):
    note = note_from_modelnote(ynote)

    # if note.sync_mark == SyncMark.NEW:
    note = note_store.createNote(token, note)

    ynote.set_sync_mark_to_normal()  # = SyncMark.NORMAL
    ynote.guid = note.guid
    ynote.usn = note.updateSequenceNum
    ynote.save()

    return ynote


def push_note_update(ynote, note_store, token, conflict_option):
    # elif note.sync_mark == SyncMark.UPDATE:
    origin_note = note_store.getNote(
        token,
        ynote.guid,
        False,  # withContent
        False,  # withResourcesData
        False,  # withResourcesRecognition
        False  # withResourcesAlternateData
    )
    if ynote.usn != origin_note.updateSequenceNum:
        logger.warning('push note %s with conflict', ynote.title)
        if conflict_option == ConflictOption.RAISE_EXCEPTION:
            raise ConflictError
        elif conflict_option == ConflictOption.FORCE_OVERWRITE:
            pass

    if ynote.deleted:
        logger.debug('deleting note %s', origin_note.title.decode('utf-8'))
        updateSequenceNum = note_store.deleteNote(token, ynote.guid)
    else:
        logger.debug('update note %s to %s', origin_note.title.decode('utf-8'), ynote.title)
        note_from_modelnote(ynote, note=origin_note)
        note = note_store.updateNote(token, origin_note)
        updateSequenceNum = note.updateSequenceNum

    ynote.set_sync_mark_to_normal()  # ynote.sync_mark = SyncMark.NORMAL
    ynote.usn = updateSequenceNum
    ynote.save()

    return ynote
