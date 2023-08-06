from django.core.management import BaseCommand

from yx.sync.fullsync import push


class Command(BaseCommand):
    def handle(self, **options):
        return push(**options)
