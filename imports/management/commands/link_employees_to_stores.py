from django.core.management.base import BaseCommand

from imports.services.employee_store_linker import link_employees_to_stores


class Command(BaseCommand):
    help = "Link employees to stores by cost center"

    def handle(self, *args, **options):
        summary = link_employees_to_stores()

        self.stdout.write(self.style.SUCCESS("Employees linked to stores"))
        self.stdout.write(str(summary))