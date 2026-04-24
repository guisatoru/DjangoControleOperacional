from django.core.paginator import Paginator
from django.db.models import Q

from stores.models import Store
from stores.services.headcount_recalculation import management_status_counts_in_headcount, names_match
from employees.models import Employee


STORES_PER_PAGE = 12
HEADCOUNT_FILTERS = ["balanced", "deficit", "excess"]


def get_base_stores_queryset():
    return Store.objects.filter(
        contracted_headcount__isnull=False,
        contracted_headcount__gt=0,
    ).order_by("name")


def apply_store_search(queryset, search):
    normalized_search = (search or "").strip()

    if not normalized_search:
        return queryset

    return queryset.filter(
        Q(name__icontains=normalized_search) |
        Q(cost_center__icontains=normalized_search) |
        Q(supervisor__icontains=normalized_search) |
        Q(coordinator__icontains=normalized_search)
    )


def apply_store_filter(queryset, selected_filter):
    if selected_filter in HEADCOUNT_FILTERS:
        return queryset.filter(headcount_status=selected_filter)

    return queryset


def count_stores_by_status(stores, status_name):
    return len([store for store in stores if store.headcount_status == status_name])


def build_store_summary(stores):
    total_contract_headcount = sum(store.contracted_headcount or 0 for store in stores)
    total_management_headcount = sum(store.management_headcount or 0 for store in stores)

    return {
        "total_stores": len(stores),
        "total_balanced": count_stores_by_status(stores, "balanced"),
        "total_deficit": count_stores_by_status(stores, "deficit"),
        "total_excess": count_stores_by_status(stores, "excess"),
        "total_contracted_headcount": total_contract_headcount,
        "total_management_headcount": total_management_headcount,
        "general_difference": total_management_headcount - total_contract_headcount,
    }


def paginate_stores(selected_filter="all", search="", page_number=1):
    base_queryset = get_base_stores_queryset()
    filtered_queryset = apply_store_filter(apply_store_search(base_queryset, search), selected_filter)

    paginator = Paginator(filtered_queryset, STORES_PER_PAGE)
    page_obj = paginator.get_page(page_number)

    return {
        "page_obj": page_obj,
        "results": list(page_obj.object_list),
        "summary": build_store_summary(list(base_queryset)),
    }


def get_store_counted_employees(store):
    counted_employees = []

    for employee in Employee.objects.filter(is_active=True).select_related("store").order_by("name"):
        if not employee.management_store_name:
            continue

        if not names_match(employee.management_store_name, store.name):
            continue

        if not management_status_counts_in_headcount(employee.management_status):
            continue

        counted_employees.append(employee)

    return counted_employees
