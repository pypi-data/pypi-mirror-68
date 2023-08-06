import json

from evernote.edam.type.ttypes import Note, NoteAttributes

ATTRS = (
    'subjectDate',
    'latitude',
    'longitude',
    'altitude',
    'author',
    'source',
    'sourceURL',
    'sourceApplication',
    'shareDate',
    'reminderOrder',
    # 'reminderDoneTime',
    # 'reminderTime',
    'placeName',
    'contentClass',
    'applicationData',
    'lastEditedBy',
    'classifications',
    'creatorId',
    'lastEditorId',
)


def NoteattributesToDict(noteattrs):
    result = {key: getattr(noteattrs, key) for key in ATTRS}

    return result


def DictToNoteattributes(dic, noteattrs=None):
    # type: (dict, NoteAttributes) -> NoteAttributes
    noteattrs = noteattrs or NoteAttributes()
    for key in dic:
        setattr(noteattrs, key, dic.get(key))
    return noteattrs


def note_from_modelnote(ynote, note=None):
    note = note or Note()

    note.guid = ynote.guid

    # title can not be starts or ends with space
    note.title = ynote.title.encode('utf-8').strip()

    note.notebookGuid = ynote.notebook.guid
    note.created = ynote.created
    note.updated = ynote.updated
    attrs = NoteAttributes()
    if ynote.attributes:
        m = json.loads(ynote.attributes)
        DictToNoteattributes(m, noteattrs=attrs)  # note.attributes)
    attrs.reminderTime = ynote.reminder_time
    attrs.reminderDoneTime = ynote.reminder_done_time
    attrs.contentClass = ynote.content_class

    note.attributes = attrs

    note.content = ynote.content
    note.deleted = ynote.deleted
    # note.updateSequenceNum=ynote.usn

    # todo: update tags
    # todo: update notebook

    return note


NOTE_ATTR_CONV = {
    'guid': 'guid',
    'title': 'title',
    'created': 'created',
    'updated': 'updated',
    'content_length': 'contentLength',
    'content': 'content',
    # 'reminder_time': 'attributes.reminderTime',
    # 'reminder_done_time': 'attributes.reminderDoneTime',
    # 'content_class': 'attributes.contentClass',
    'deleted': 'deleted',
    'usn': 'updateSequenceNum',
}


def note_to_model_dict(note):
    r = {
        key: getattr(note, key2) for key, key2 in NOTE_ATTR_CONV.iteritems()
    }
    if note.attributes:
        r['attributes'] = NoteattributesToDict(note.attributes)
        r['reminder_time'] = note.attributes.reminderTime
        r['reminder_done_time'] = note.attributes.reminderDoneTime
        r['content_class'] = note.attributes.contentClass
    r['deleted'] = bool(note.deleted)
    return r
