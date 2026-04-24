from stores.models import Store
from employees.services.derived_fields import refresh_employee_and_store_derived_fields


STORE_UPDATE_FIELDS = [
    "name",
    "geo_name",
    "contracted_headcount",
    "client",
    "state",
    "zip_code",
    "street",
    "neighborhood",
    "city",
    "is_active",
]


def build_store_field_values(store_data):
    return {
        "name": store_data.get("name"),
        "geo_name": store_data.get("geo_name"),
        "contracted_headcount": store_data.get("contracted_headcount") or None,
        "client": store_data.get("client"),
        "state": store_data.get("state"),
        "zip_code": store_data.get("zip_code"),
        "street": store_data.get("street"),
        "neighborhood": store_data.get("neighborhood"),
        "city": store_data.get("city"),
        "is_active": store_data.get("is_active"),
    }


def apply_field_values(instance, field_values):
    has_changes = False

    for field_name, new_value in field_values.items():
        if getattr(instance, field_name) != new_value:
            setattr(instance, field_name, new_value)
            has_changes = True

    return has_changes


def import_stores_from_mother_table(parsed_stores):
    summary = {
        "total": 0,
        "created": 0,
        "updated": 0,
        "unchanged": 0,
        "skipped": 0,
    }

    existing_stores = {
        store.cost_center: store
        for store in Store.objects.all()
    }

    stores_to_create = []
    stores_to_update = []

    for store_data in parsed_stores:
        summary["total"] += 1

        cost_center = store_data.get("cost_center")

        if not cost_center:
            summary["skipped"] += 1
            continue

        field_values = build_store_field_values(store_data)

        store = existing_stores.get(cost_center)

        if not store:
            stores_to_create.append(Store(cost_center=cost_center, **field_values))
            summary["created"] += 1
            continue

        if apply_field_values(store, field_values):
            stores_to_update.append(store)
            summary["updated"] += 1
        else:
            summary["unchanged"] += 1

    if stores_to_create:
        Store.objects.bulk_create(stores_to_create)

    if stores_to_update:
        Store.objects.bulk_update(stores_to_update, STORE_UPDATE_FIELDS)

    refresh_employee_and_store_derived_fields()

    return summary
