from core.utils.normalizers import normalize_column_name
from stores.models import Store


def normalize_store_match(value):
    return normalize_column_name(value)


def import_management_supervision(parsed_stores):
    summary = {
        "total_management_records": 0,
        "active_system_stores": 0,
        "updated": 0,
        "unchanged": 0,
        "active_system_not_found_in_management": 0,
        "skipped": 0,
    }

    management_by_store_name = {
        normalize_store_match(store_data.get("store_name")): store_data
        for store_data in parsed_stores
        if store_data.get("store_name")
    }

    summary["total_management_records"] = len(parsed_stores)

    stores = list(Store.objects.filter(is_active=True))
    summary["active_system_stores"] = len(stores)
    stores_to_update = []

    for store in stores:
        store_data = management_by_store_name.get(normalize_store_match(store.name))

        if not store_data:
            summary["active_system_not_found_in_management"] += 1
            continue

        field_values = {
            "supervisor": store_data.get("supervisor"),
            "coordinator": store_data.get("coordinator"),
        }

        has_changes = False

        for field_name, new_value in field_values.items():
            if getattr(store, field_name) != new_value:
                setattr(store, field_name, new_value)
                has_changes = True

        if has_changes:
            stores_to_update.append(store)
            summary["updated"] += 1
        else:
            summary["unchanged"] += 1

    if stores_to_update:
        Store.objects.bulk_update(stores_to_update, ["supervisor", "coordinator"])

    return summary
