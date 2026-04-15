from django.core.management.base import BaseCommand

from imports.parsers.mother_table_parser import parse_mother_table_file


class Command(BaseCommand):
    help = "Test mother table parser"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        file_path = options["file_path"]

        stores = parse_mother_table_file(file_path)

        self.stdout.write(self.style.SUCCESS(f"Total stores parsed: {len(stores)}"))

        for store in stores[:10]:
            self.stdout.write(str(store))