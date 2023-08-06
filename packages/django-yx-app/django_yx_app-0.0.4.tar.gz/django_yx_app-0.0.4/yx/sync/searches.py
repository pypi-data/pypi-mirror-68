from yx.sync.fullsync import ConflictOption
from yx.sync.notes import save_note_in_local_db


def cache_search_result(search_result, account):
    notes = []
    for note in search_result.notes:
        yxnote = save_note_in_local_db(note, account, ConflictOption.FORCE_OVERWRITE)
        notes.append(yxnote)
    return notes
