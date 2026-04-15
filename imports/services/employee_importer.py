from employees.models import Employee


def import_employees_from_totvs(parsed_employees):
    summary = {
        "total": 0,
        "created": 0,
        "updated": 0,
        "skipped": 0,
    }

    for employee_data in parsed_employees:
        summary["total"] += 1

        employee_code = employee_data.get("employee_code")

        if not employee_code:
            summary["skipped"] += 1
            continue

        employee, created = Employee.objects.update_or_create(
            employee_code=employee_code,
            defaults={
                "name": employee_data.get("name"),
                "cost_center": employee_data.get("cost_center"),
                "totvs_job_title": employee_data.get("totvs_job_title"),
                "payroll_status": employee_data.get("payroll_status"),
                "admission_date": employee_data.get("admission_date"),
                "first_contract_end_date": employee_data.get("first_contract_end_date"),
                "second_contract_end_date": employee_data.get("second_contract_end_date"),
                "dismissal_date": employee_data.get("dismissal_date"),
                "is_active": employee_data.get("is_active"),
            }
        )

        if created:
            summary["created"] += 1
        else:
            summary["updated"] += 1

    return summary