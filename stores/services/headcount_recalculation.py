from core.utils.normalizers import normalize_column_name
from employees.models import Employee
from stores.models import Store


MANAGEMENT_STATUSES_THAT_COUNT = [
    "ATIVO",
    "AVISO",
    "FERIAS",
]


def management_status_counts_in_headcount(status):
    normalized_status = normalize_column_name(status)
    return normalized_status in MANAGEMENT_STATUSES_THAT_COUNT


def names_match(first_name, second_name):
    normalized_first_name = normalize_column_name(first_name)
    normalized_second_name = normalize_column_name(second_name)
    return normalized_first_name == normalized_second_name


def recalculate_store_headcount_data():
    stores = list(
        Store.objects.filter(
            contracted_headcount__isnull=False,
            contracted_headcount__gt=0,
        ).order_by("name")
    )

    employees = Employee.objects.only("management_store_name", "management_status")

    counts_by_store_name = {}

    for employee in employees:
        if not employee.management_store_name:
            continue

        if not management_status_counts_in_headcount(employee.management_status):
            continue

        normalized_store_name = normalize_column_name(employee.management_store_name)
        counts_by_store_name[normalized_store_name] = counts_by_store_name.get(normalized_store_name, 0) + 1

    stores_to_update = []

    for store in stores:
        management_headcount = counts_by_store_name.get(normalize_column_name(store.name), 0)

        if management_headcount == 0:
            store.management_headcount = 0
            store.headcount_difference = 0
            store.headcount_status = "ignored"
        else:
            store.management_headcount = management_headcount
            store.headcount_difference = management_headcount - (store.contracted_headcount or 0)

            if store.headcount_difference > 0:
                store.headcount_status = "excess"
            elif store.headcount_difference < 0:
                store.headcount_status = "deficit"
            else:
                store.headcount_status = "balanced"

        stores_to_update.append(store)

    if stores_to_update:
        Store.objects.bulk_update(
            stores_to_update,
            ["management_headcount", "headcount_difference", "headcount_status"],
        )
