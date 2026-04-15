from django.core.management.base import BaseCommand

from imports.parsers.totvs_parser import parse_totvs_file


class Command(BaseCommand):
    help = "Test TOTVS parser"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        file_path = options["file_path"]

        employees = parse_totvs_file(file_path)

        self.stdout.write(self.style.SUCCESS(f"Total employees parsed: {len(employees)}"))

        for employee in employees[:10]:
            self.stdout.write(str(employee))