from stores.models import Store


def import_stores_from_mother_table(parsed_stores):
    summary = {
        "total": 0,
        "created": 0,
        "updated": 0,
        "skipped": 0,
    }

    for store_data in parsed_stores:
        summary["total"] += 1

        cost_center = store_data.get("cost_center")

        if not cost_center:
            summary["skipped"] += 1
            continue

        store, created = Store.objects.update_or_create(
            cost_center=cost_center,
            defaults={
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
        )

        if created:
            summary["created"] += 1
        else:
            summary["updated"] += 1

    return summary