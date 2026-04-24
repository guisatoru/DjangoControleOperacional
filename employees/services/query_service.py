from django.core.paginator import Paginator
from django.db.models import Q

from employees.models import DismissalRecord, Employee


EMPLOYEES_PER_PAGE = 12
EMPLOYEE_FILTER_TO_FIELD = {
    "management_duplicate": "has_management_duplicate_cached",
    "store_divergence": "has_store_divergence_cached",
    "job_title_divergence": "has_job_title_divergence_cached",
    "status_divergence": "has_status_divergence_cached",
}


def get_base_employees_queryset():
    dismissed_employee_ids = DismissalRecord.objects.values_list("employee_id", flat=True)
    return Employee.objects.filter(is_active=True).exclude(id__in=dismissed_employee_ids).select_related("store").order_by("name")


def apply_employee_search(queryset, search):
    normalized_search = (search or "").strip()

    if not normalized_search:
        return queryset

    return queryset.filter(
        Q(name__icontains=normalized_search) |
        Q(employee_code__icontains=normalized_search)
    )


def build_employee_summary(base_queryset):
    return {
        "total_employees": base_queryset.count(),
        "total_store_divergences": base_queryset.filter(has_store_divergence_cached=True).count(),
        "total_job_title_divergences": base_queryset.filter(has_job_title_divergence_cached=True).count(),
        "total_status_divergences": base_queryset.filter(has_status_divergence_cached=True).count(),
        "total_management_duplicates": base_queryset.filter(has_management_duplicate_cached=True).count(),
        "total_only_totvs": base_queryset.filter(has_management_data_cached=False).count(),
    }


def get_employee_summary():
    base_queryset = get_base_employees_queryset()
    return build_employee_summary(base_queryset)


def apply_employee_filter(queryset, selected_filter):
    if selected_filter == "only_totvs":
        return queryset.filter(has_management_data_cached=False)

    field_name = EMPLOYEE_FILTER_TO_FIELD.get(selected_filter)

    if not field_name:
        return queryset

    return queryset.filter(**{field_name: True})


def paginate_employees(selected_filter="all", search="", page_number=1):
    base_queryset = get_base_employees_queryset()
    searched_queryset = apply_employee_search(base_queryset, search)
    filtered_queryset = apply_employee_filter(searched_queryset, selected_filter)

    paginator = Paginator(filtered_queryset, EMPLOYEES_PER_PAGE)
    page_obj = paginator.get_page(page_number)
    page_results = list(page_obj.object_list)

    return {
        "page_obj": page_obj,
        "results": page_results,
    }
