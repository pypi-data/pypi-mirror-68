from django.core.management.base import BaseCommand
from django.utils.translation import ugettext as _

from ...util.xml.xml import untis_import_xml


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("untis_xml_path", help=_("Path to Untis XML export file"))

    def handle(self, *args, **options):
        untis_xml = open(options["untis_xml_path"], "rb")

        untis_import_xml(None, untis_xml)
