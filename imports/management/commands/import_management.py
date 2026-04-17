from django.core.management.base import BaseCommand

from imports.parsers.management_parser import (
    parse_management_employees_file,
    parse_management_supervision_file,
)
from imports.services.management_employee_importer import import_management_employees
from imports.services.management_supervision_importer import import_management_supervision


class Command(BaseCommand):
    help = "Import management data"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        file_path = options["file_path"]

        employees = parse_management_employees_file(file_path)
        employee_summary = import_management_employees(employees)

        stores = parse_management_supervision_file(file_path)
        supervision_summary = import_management_supervision(stores)

        self.stdout.write(self.style.SUCCESS("Management import completed"))

        self.stdout.write("")
        self.stdout.write("Employees:")
        self.stdout.write(str(employee_summary))

        self.stdout.write("")
        self.stdout.write("Supervision:")
        self.stdout.write(str(supervision_summary))