from django.core.management.base import BaseCommand

from employees.services.derived_fields import refresh_employee_and_store_derived_fields


class Command(BaseCommand):
    help = "Refresh cached employee flags and store headcount fields"

    def handle(self, *args, **options):
        refresh_employee_and_store_derived_fields()
        self.stdout.write(self.style.SUCCESS("Derived data refreshed successfully."))
