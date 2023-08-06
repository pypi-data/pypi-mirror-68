import logging
from optparse import make_option

from django.core.management import BaseCommand
from django.db import transaction

from yx.models import YUser
from yx.utils import cache_note

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--token', dest='token'),
    )

    @transaction.atomic
    def handle(self, *guids, **options):
        account = YUser.objects.get(token=options['token'])
        client = account.get_client()
        note_store = client.get_note_store()

        for guid in guids:
            # note = Yxnote.objects.get(guid=guid)

            # update note content with resource data

            # download resources
            notedata = note_store.getNote(
                account.decrypted_token, guid,
                True,  # withContent
                False,  # withResourcesData
                False,  # withResourcesRecognition
                False  # withResourcesAlternateData
            )

            cache_note(account, notedata)

        # fixme: do not download resource now
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
