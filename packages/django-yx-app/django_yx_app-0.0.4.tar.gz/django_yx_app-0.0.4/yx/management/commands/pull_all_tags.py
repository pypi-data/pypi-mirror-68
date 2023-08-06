from optparse import make_option

from django.core.management import BaseCommand

from yx.sync.tags import pullalltags


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--username', dest='username'),
    )

    def handle(self, **options):
        return pullalltags(**options)
