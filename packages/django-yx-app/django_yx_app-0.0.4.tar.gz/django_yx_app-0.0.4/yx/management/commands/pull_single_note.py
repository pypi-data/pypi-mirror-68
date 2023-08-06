from optparse import make_option

from django.core.management import BaseCommand

from yx.sync.fullsync import pullsinglenote


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--token', dest='token'),
        make_option('--guids', nargs='+'),
    )

    def handle(self, *guids, **options):
        for guid in guids:
            pullsinglenote(guid, **options)
