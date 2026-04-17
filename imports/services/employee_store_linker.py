from employees.models import Employee
from stores.models import Store


def link_employees_to_stores():
    summary = {
        "total_employees": 0,
        "linked": 0,
        "not_found": 0,
        "without_cost_center": 0,
    }

    stores_by_cost_center = {
        store.cost_center: store
        for store in Store.objects.filter(is_active=True)
    }

    employees = Employee.objects.filter(is_active=True)

    for employee in employees:
        summary["total_employees"] += 1

        if not employee.cost_center:
            summary["without_cost_center"] += 1
            employee.store = None
            employee.save(update_fields=["store"])
            continue

        store = stores_by_cost_center.get(employee.cost_center)

        if store:
            employee.store = store
            employee.save(update_fields=["store"])
            summary["linked"] += 1
        else:
            employee.store = None
            employee.save(update_fields=["store"])
            summary["not_found"] += 1

    return summary