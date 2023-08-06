import logging

from yx.djangohelper import update_or_create
from yx.models import YNotebook

logger = logging.getLogger('yx.sync')


def cache_notebook(notebook, account):
    logger.debug('notebook=%s', notebook.name.decode('utf-8'))
    ynb, create = update_or_create(
        YNotebook.objects,
        guid=notebook.guid,
        defaults=dict(
            name=notebook.name.decode('utf-8'),
            usn=notebook.updateSequenceNum,
        )
    )
    ynb.set_sync_mark_to_normal()  # ynb.sync_mark = SyncMark.NORMAL
    ynb.name = notebook.name.decode('utf-8')
    ynb.usn = notebook.updateSequenceNum
    ynb.save()

    return ynb
