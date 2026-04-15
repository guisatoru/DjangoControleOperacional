from django.core.management.base import BaseCommand

from imports.parsers.mother_table_parser import parse_mother_table_file
from imports.services.store_importer import import_stores_from_mother_table


class Command(BaseCommand):
    help = "Import stores from mother table"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        file_path = options["file_path"]

        stores = parse_mother_table_file(file_path)
        summary = import_stores_from_mother_table(stores)

        self.stdout.write(self.style.SUCCESS("Mother table import completed"))
        self.stdout.write(str(summary))