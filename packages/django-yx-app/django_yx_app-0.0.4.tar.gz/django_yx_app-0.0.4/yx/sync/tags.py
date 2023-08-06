import logging

from yx.djangohelper import update_or_create
from yx.models import YUser

logger = logging.getLogger('yx.sync')


def pullalltags(username, *args, **options):
    account = YUser.objects.get(username=username)
    client = account.get_client()
    note_store = client.get_note_store()
    tags = note_store.listTags(account.token)

    for tag in tags:
        yxt, _created = update_or_create(
            account.tags,
            guid=tag.guid,
            defaults=dict(
                name=tag.name.decode('utf-8')
            )
        )
        logger.info('create tag %s', yxt.guid)


def pull_a_tag(account, tag):
    logger.debug('save tag "%s"', tag.name.decode('utf-8'))
    yxtag, created = update_or_create(
        account.tags,
        guid=tag.guid,
        defaults=dict(
            name=tag.name.decode('utf-8'),
            usn=tag.updateSequenceNum,
        )
    )
    yxtag.set_sync_mark_to_normal()  # yxtag.sync_mark = SyncMark.NORMAL
    yxtag.name = tag.name.decode('utf-8')
    yxtag.notes.clear()
    yxtag.save()

    return yxtag
