from django.core.management.base import BaseCommand

from imports.parsers.management_parser import (
    parse_management_employees_file,
    parse_management_supervision_file,
)


class Command(BaseCommand):
    help = "Test management parser"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        file_path = options["file_path"]

        employees = parse_management_employees_file(file_path)
        stores = parse_management_supervision_file(file_path)

        self.stdout.write(self.style.SUCCESS(f"Total management employees parsed: {len(employees)}"))
        for employee in employees[:10]:
            self.stdout.write(str(employee))

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(f"Total supervision stores parsed: {len(stores)}"))
        for store in stores[:10]:
            self.stdout.write(str(store))