from django.core.management.base import BaseCommand

from imports.parsers.totvs_parser import parse_totvs_file
from imports.services.employee_importer import import_employees_from_totvs


class Command(BaseCommand):
    help = "Import employees from TOTVS CSV"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        file_path = options["file_path"]

        employees = parse_totvs_file(file_path)
        summary = import_employees_from_totvs(employees)

        self.stdout.write(self.style.SUCCESS("TOTVS import completed"))
        self.stdout.write(str(summary))