from employees.models import Employee
from stores.models import Store


def import_employees_from_totvs(parsed_employees):
    summary = {
        "total": 0,
        "created": 0,
        "updated": 0,
        "unchanged": 0,
        "skipped": 0,
        "linked_to_store": 0,
        "store_not_found": 0,
        "without_cost_center": 0,
    }

    stores_by_cost_center = {
        store.cost_center: store
        for store in Store.objects.all()
    }

    for employee_data in parsed_employees:
        summary["total"] += 1

        employee_code = employee_data.get("employee_code")

        if not employee_code:
            summary["skipped"] += 1
            continue

        is_active = employee_data.get("is_active")
        cost_center = employee_data.get("cost_center")

        store = None

        if is_active:
            if cost_center:
                store = stores_by_cost_center.get(cost_center)

                if store:
                    summary["linked_to_store"] += 1
                else:
                    summary["store_not_found"] += 1
            else:
                summary["without_cost_center"] += 1

        defaults = {
            "name": employee_data.get("name"),
            "cost_center": cost_center,
            "store": store,
            "totvs_job_title": employee_data.get("totvs_job_title"),
            "payroll_status": employee_data.get("payroll_status"),
            "admission_date": employee_data.get("admission_date"),
            "first_contract_end_date": employee_data.get("first_contract_end_date"),
            "second_contract_end_date": employee_data.get("second_contract_end_date"),
            "dismissal_date": employee_data.get("dismissal_date"),
            "is_active": is_active,
            "counts_in_store_headcount": employee_data.get("counts_in_store_headcount"),
        }

        employee = Employee.objects.filter(employee_code=employee_code).first()

        if not employee:
            Employee.objects.create(
                employee_code=employee_code,
                **defaults
            )
            summary["created"] += 1
            continue

        changed_fields = []

        for field, new_value in defaults.items():
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