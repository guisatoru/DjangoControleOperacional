from stores.models import Store
from core.utils.normalizers import normalize_column_name


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

    stores = Store.objects.filter(is_active=True)
    summary["active_system_stores"] = stores.count()

    for store in stores:
        store_data = management_by_store_name.get(
            normalize_store_match(store.name)
        )

        if not store_data:
            summary["active_system_not_found_in_management"] += 1
            continue

        fields_from_management = {
            "supervisor": store_data.get("supervisor"),
            "coordinator": store_data.get("coordinator"),
        }

        changed_fields = []

        for field, new_value in fields_from_management.items():
            current_value = getattr(store, field)

            if current_value != new_value:
                setattr(store, field, new_value)
                changed_fields.append(field)

        if changed_fields:
            store.save(update_fields=changed_fields)
            summary["updated"] += 1
        else:
            summary["unchanged"] += 1

    return summary