from django.core.paginator import Paginator
from django.db.models import Q

from employees.models import DismissalRecord


DISMISSALS_PER_PAGE = 12


def get_base_dismissals_queryset():
    return DismissalRecord.objects.order_by("-dismissal_date", "name")


def apply_dismissal_search(queryset, search):
    normalized_search = (search or "").strip()

    if not normalized_search:
        return queryset

    return queryset.filter(
        Q(name__icontains=normalized_search) |
        Q(employee_code__icontains=normalized_search) |
        Q(management_status__icontains=normalized_search) |
        Q(payroll_status__icontains=normalized_search)
    )


def apply_dismissal_filter(queryset, selected_filter):
    if selected_filter == "ok":
        return queryset.filter(comparison_status="ok")

    if selected_filter == "pending":
        return queryset.filter(comparison_status="pending")

    if selected_filter == "divergent":
        return queryset.filter(comparison_status="divergent")

    return queryset


def build_dismissal_summary(base_queryset):
    return {
        "total_dismissals": base_queryset.count(),
        "total_ok": base_queryset.filter(comparison_status="ok").count(),
        "total_pending": base_queryset.filter(comparison_status="pending").count(),
        "total_divergent": base_queryset.filter(comparison_status="divergent").count(),
    }


def paginate_dismissals(selected_filter="all", search="", page_number=1):
    base_queryset = get_base_dismissals_queryset()
    filtered_queryset = apply_dismissal_filter(apply_dismissal_search(base_queryset, search), selected_filter)

    paginator = Paginator(filtered_queryset, DISMISSALS_PER_PAGE)
    page_obj = paginator.get_page(page_number)

    return {
        "page_obj": page_obj,
        "results": list(page_obj.object_list),
        "summary": build_dismissal_summary(base_queryset),
    }
