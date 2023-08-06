import logging

from evernote.edam.type.ttypes import Note

from yx.models import YNote, YTag, YNotebook, YUser

logger = logging.getLogger(__name__)


def cache_note(yxaccount, note):
    # type: (YUser, Note) -> YNote
    """
    cache note from evernote api into database
    """

    logger.debug('cache_note title=%s', note.title.decode('utf-8'))

    notebookGuid = note.notebookGuid
    notebook, created = YNotebook.objects.get_or_create(
        guid=notebookGuid, defaults=dict(
            yxaccount=yxaccount,
            name=notebookGuid
        ))

    # store into db
    yxnote, _created = YNote.objects.get_or_create(
        guid=note.guid,
        defaults=dict(
            yxaccount=yxaccount,
            notebook=notebook,
        ))
    logger.debug('create note(%s) in database', yxnote.guid)

    yxnote.notebook = notebook
    yxnote.yxaccount = yxaccount

    # copy fields
    yxnote.guid = note.guid
    yxnote.title = note.title
    yxnote.created = note.created
    yxnote.updated = note.updated
    yxnote.attributes = note.attributes

    yxnote.deleted = note.deleted or False
    logger.debug('note deleted=%s', note.deleted)
    yxnote.usn = note.updateSequenceNum

    # note.attributes
    yxnote.reminder_time = note.attributes.reminderTime
    yxnote.reminder_done_time = note.attributes.reminderDoneTime

    yxnote.save()

    # download tags
    newtags = []
    for tagguid in getattr(note, 'tagGuids') or []:
        logger.debug('tagguid=%s', tagguid)
        tag, _created = YTag.objects.get_or_create(guid=tagguid, yxaccount=yxaccount)
        newtags.append(tag)
    yxnote.tags.clear()
    yxnote.tags.add(*newtags)

    return yxnote


def pull_a_tag(account, tag):
    yxtag, created = account.tags.get_or_create(guid=tag.guid)
    yxtag.name = tag.name.decode('utf-8')
    yxtag.notes.clear()
    yxtag.save()

    return tag


def cache_search_result(account, search_result):
    notes = []
    for note in search_result.notes:
        yxnote = cache_note(account, note)
        notes.append(yxnote)
    return notes
