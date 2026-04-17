from stores.models import Store


def import_stores_from_mother_table(parsed_stores):
    summary = {
        "total": 0,
        "created": 0,
        "updated": 0,
        "unchanged": 0,
        "skipped": 0,
    }

    for store_data in parsed_stores:
        summary["total"] += 1

        cost_center = store_data.get("cost_center")

        if not cost_center:
            summary["skipped"] += 1
            continue

        defaults = {
            "name": store_data.get("name"),
            "geo_name": store_data.get("geo_name"),
            "contracted_headcount": store_data.get("contracted_headcount") or None,
            "client": store_data.get("client"),
            "state": store_data.get("state"),
            "zip_code": store_data.get("zip_code"),
            "street": store_data.get("street"),
            "neighborhood": store_data.get("neighborhood"),
            "is_active": store_data.get("is_active"),
        }

        store = Store.objects.filter(cost_center=cost_center).first()

        if not store:
            Store.objects.create(
                cost_center=cost_center,
                **defaults
            )
            summary["created"] += 1
            continue

        has_changes = False

        for field, new_value in defaults.items():
            current_value = getattr(store, field)

            if current_value != new_value:
                setattr(store, field, new_value)
                has_changes = True

        if has_changes:
            store.save(update_fields=list(defaults.keys()))
            summary["updated"] += 1
        else:
            summary["unchanged"] += 1

    return summary