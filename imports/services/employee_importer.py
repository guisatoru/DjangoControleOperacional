from employees.models import Employee
from employees.services.derived_fields import refresh_employee_and_store_derived_fields
from stores.models import Store


EMPLOYEE_UPDATE_FIELDS = [
    "name",
    "cost_center",
    "store",
    "totvs_job_title",
    "payroll_status",
    "admission_date",
    "first_contract_end_date",
    "second_contract_end_date",
    "dismissal_date",
    "is_active",
    "counts_in_store_headcount",
]


def build_totvs_field_values(employee_data, store):
    return {
        "name": employee_data.get("name"),
        "cost_center": employee_data.get("cost_center"),
        "store": store,
        "totvs_job_title": employee_data.get("totvs_job_title"),
        "payroll_status": employee_data.get("payroll_status"),
        "admission_date": employee_data.get("admission_date"),
        "first_contract_end_date": employee_data.get("first_contract_end_date"),
        "second_contract_end_date": employee_data.get("second_contract_end_date"),
        "dismissal_date": employee_data.get("dismissal_date"),
        "is_active": employee_data.get("is_active"),
        "counts_in_store_headcount": employee_data.get("counts_in_store_headcount"),
    }


def apply_field_values(instance, field_values):
    has_changes = False

    for field_name, new_value in field_values.items():
        if getattr(instance, field_name) != new_value:
            setattr(instance, field_name, new_value)
            has_changes = True

    return has_changes


def resolve_store_for_active_employee(employee_data, stores_by_cost_center, summary):
    if not employee_data.get("is_active"):
        return None

    cost_center = employee_data.get("cost_center")

    if not cost_center:
        summary["without_cost_center"] += 1
        return None

    store = stores_by_cost_center.get(cost_center)

    if store:
        summary["linked_to_store"] += 1
    else:
        summary["store_not_found"] += 1

    return store


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

    existing_employees = {
        employee.employee_code: employee
        for employee in Employee.objects.select_related("store").all()
    }

    employees_to_create = []
    employees_to_update = []

    for employee_data in parsed_employees:
        summary["total"] += 1

        employee_code = employee_data.get("employee_code")

        if not employee_code:
            summary["skipped"] += 1
            continue

        store = resolve_store_for_active_employee(employee_data, stores_by_cost_center, summary)
        field_values = build_totvs_field_values(employee_data, store)

        employee = existing_employees.get(employee_code)

        if not employee:
            employees_to_create.append(Employee(employee_code=employee_code, **field_values))
            summary["created"] += 1
            continue

        if apply_field_values(employee, field_values):
            employees_to_update.append(employee)
            summary["updated"] += 1
        else:
            summary["unchanged"] += 1

    if employees_to_create:
        Employee.objects.bulk_create(employees_to_create)

    if employees_to_update:
        Employee.objects.bulk_update(employees_to_update, EMPLOYEE_UPDATE_FIELDS)

    refresh_employee_and_store_derived_fields()

    return summary
