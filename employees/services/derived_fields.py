from employees.models import Employee
from employees.services.dismissal_sync import sync_dismissal_records
from employees.services.termination_service import refresh_termination_cache_fields
from stores.services.headcount_recalculation import recalculate_store_headcount_data


DERIVED_EMPLOYEE_FIELDS = [
    "has_store_divergence_cached",
    "has_job_title_divergence_cached",
    "has_status_divergence_cached",
    "has_management_duplicate_cached",
    "has_management_data_cached",
]
DERIVED_FIELDS_BATCH_SIZE = 500


def apply_derived_fields(employee):
    employee.has_store_divergence_cached = employee.has_store_divergence()
    employee.has_job_title_divergence_cached = employee.has_job_title_divergence()
    employee.has_status_divergence_cached = employee.has_status_divergence()
    employee.has_management_duplicate_cached = employee.has_management_duplicate_records()
    employee.has_management_data_cached = bool(employee.management_status)


def refresh_employee_derived_fields():
    employees = list(Employee.objects.select_related("store").all())
    employees_to_update = []

    for employee in employees:
        previous_values = {
            field_name: getattr(employee, field_name)
            for field_name in DERIVED_EMPLOYEE_FIELDS
        }

        apply_derived_fields(employee)

        has_changes = any(
            getattr(employee, field_name) != previous_values[field_name]
            for field_name in DERIVED_EMPLOYEE_FIELDS
        )

        if has_changes:
            employees_to_update.append(employee)

    if employees_to_update:
        for start_index in range(0, len(employees_to_update), DERIVED_FIELDS_BATCH_SIZE):
            batch = employees_to_update[start_index:start_index + DERIVED_FIELDS_BATCH_SIZE]
            Employee.objects.bulk_update(batch, DERIVED_EMPLOYEE_FIELDS)


def refresh_employee_and_store_derived_fields():
    refresh_employee_derived_fields()
    refresh_termination_cache_fields()
    recalculate_store_headcount_data()
    sync_dismissal_records()
