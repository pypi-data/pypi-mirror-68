# a search
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec
from evernote.edam.type.ttypes import NoteSortOrder


class Search(object):

    def __init__(self, yuser, words):
        self.yuser = yuser
        self.words = words

    def search(self):
        # words = words.encode('utf-8') if isinstance(words, unicode) else words

        client = self.yuser.get_client()  # yxappsettings.get_client(token=self.decrypted_token)

        note_store = client.get_note_store()

        fltr = NoteFilter()
        fltr.words = self.words.encode('utf-8')
        fltr.order = NoteSortOrder.CREATED
        fltr.ascending = True

        spec = NotesMetadataResultSpec()
        spec.includeTitle = True
        spec.includeCreated = True
        spec.includeUpdateSequenceNum = True
        spec.includeTagGuids = True

        search_result = note_store.findNotesMetadata(self.yuser.decrypted_token, fltr, 0, 5000, spec)

        return search_result
