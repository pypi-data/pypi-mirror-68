import logging
from optparse import make_option

from django.core.management import BaseCommand
from django.db import transaction

from yx.models import YUser

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--username', dest='username'),
    )

    @transaction.atomic
    def handle(self, username, *args, **options):
        account = YUser.objects.get(username=username)
        synctag(account)


def synctag(account):
    client = account.get_client()
    note_store = client.get_note_store()
    tags = note_store.listTags(account.decrypted_token)

    for tag in tags:
        yxt, _created = account.tags.create_or_update(guid=tag.guid, defaults=dict(name=tag.name.decode('utf-8')))
        logger.info('create tag %s', yxt.guid)
