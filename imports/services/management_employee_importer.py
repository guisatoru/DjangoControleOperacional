from employees.models import Employee
from employees.services.derived_fields import refresh_employee_and_store_derived_fields


MANAGEMENT_UPDATE_FIELDS = [
    "management_store_name",
    "management_job_title",
    "management_status",
    "management_records_count",
    "management_non_transferred_records_count",
    "management_non_transferred_statuses",
]


def build_management_field_values(employee_data):
    return {
        "management_store_name": employee_data.get("management_store_name"),
        "management_job_title": employee_data.get("management_job_title"),
        "management_status": employee_data.get("management_status"),
        "management_records_count": employee_data.get("management_records_count", 0),
        "management_non_transferred_records_count": employee_data.get("management_non_transferred_records_count", 0),
        "management_non_transferred_statuses": employee_data.get("management_non_transferred_statuses", []),
    }


def apply_field_values(instance, field_values):
    has_changes = False

    for field_name, new_value in field_values.items():
        if getattr(instance, field_name) != new_value:
            setattr(instance, field_name, new_value)
            has_changes = True

    return has_changes


def import_management_employees(parsed_employees):
    summary = {
        "total_management_records": 0,
        "system_employee_records": 0,
        "updated": 0,
        "unchanged": 0,
        "system_not_found_in_management": 0,
        "skipped": 0,
    }

    management_by_employee_code = {
        employee_data.get("employee_code"): employee_data
        for employee_data in parsed_employees
        if employee_data.get("employee_code")
    }

    summary["total_management_records"] = len(parsed_employees)

    employees = list(Employee.objects.all())
    summary["system_employee_records"] = len(employees)
    employees_to_update = []

    for employee in employees:
        employee_data = management_by_employee_code.get(employee.employee_code)

        if not employee_data:
            summary["system_not_found_in_management"] += 1
            continue

        field_values = build_management_field_values(employee_data)

        if apply_field_values(employee, field_values):
            employees_to_update.append(employee)
            summary["updated"] += 1
        else:
            summary["unchanged"] += 1

    if employees_to_update:
        Employee.objects.bulk_update(employees_to_update, MANAGEMENT_UPDATE_FIELDS)

    refresh_employee_and_store_derived_fields()
    return summary
