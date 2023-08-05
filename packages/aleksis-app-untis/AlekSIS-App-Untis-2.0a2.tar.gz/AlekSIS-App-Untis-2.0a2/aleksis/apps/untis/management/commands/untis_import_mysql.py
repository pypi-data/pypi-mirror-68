from django.core.management.base import BaseCommand

from ...tasks import untis_import_mysql


class Command(BaseCommand):
    def handle(self, *args, **options):
        untis_import_mysql()
