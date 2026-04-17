from employees.models import Employee


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

    employees = Employee.objects.all()

    summary["system_employee_records"] = employees.count()

    for employee in employees:
        employee_data = management_by_employee_code.get(employee.employee_code)

        if not employee_data:
            summary["system_not_found_in_management"] += 1
            continue

        fields_from_management = {
            "management_store_name": employee_data.get("management_store_name"),
            "management_job_title": employee_data.get("management_job_title"),
            "management_status": employee_data.get("management_status"),
            "management_records_count": employee_data.get("management_records_count", 0),
            "management_non_transferred_records_count": employee_data.get("management_non_transferred_records_count", 0),
            "management_non_transferred_statuses": employee_data.get("management_non_transferred_statuses", []),
        }

        changed_fields = []

        for field, new_value in fields_from_management.items():
            current_value = getattr(employee, field)

            if current_value != new_value:
                setattr(employee, field, new_value)
                changed_fields.append(field)

        if changed_fields:
            employee.save(update_fields=changed_fields)
            summary["updated"] += 1
        else:
            summary["unchanged"] += 1

    return summary