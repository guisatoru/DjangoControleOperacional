from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Employee


def divergences_view(request):
    management_duplicates = [
        employee for employee in Employee.objects.all()
        if employee.has_management_duplicate_records()
    ]

    store_divergences = [
        employee for employee in Employee.objects.filter(is_active=True)
        if employee.has_store_divergence()
    ]

    status_divergences = [
        employee for employee in Employee.objects.exclude(payroll_status="D")
        if employee.has_status_divergence()
    ]

    context = {
        "management_duplicates": management_duplicates,
        "store_divergences": store_divergences,
        "status_divergences": status_divergences,
    }

    return render(request, "employees/divergences.html", context)


def dismissals_view(request):
    dismissed_employees = Employee.objects.filter(
        payroll_status="D"
    ).order_by("-dismissal_date", "name")

    dismissal_divergences = [
        employee for employee in dismissed_employees
        if employee.has_status_divergence()
    ]

    context = {
        "dismissed_employees": dismissed_employees,
        "dismissal_divergences": dismissal_divergences,
    }

    return render(request, "employees/dismissals.html", context)

def employees_list_view(request):
    selected_filter = request.GET.get("filter", "all")
    search = request.GET.get("search", "").strip()

    employees = Employee.objects.filter(is_active=True).select_related("store").order_by("name")

    if search:
        employees = employees.filter(
            Q(name__icontains=search) |
            Q(employee_code__icontains=search)
    )

    employees_list = list(employees)

    if selected_filter == "store_divergence":
        employees_list = [
            employee for employee in employees_list
            if employee.has_store_divergence()
        ]

    elif selected_filter == "status_divergence":
        employees_list = [
            employee for employee in employees_list
            if employee.has_status_divergence()
        ]

    elif selected_filter == "management_duplicate":
        employees_list = [
            employee for employee in employees_list
            if employee.has_management_duplicate_records()
        ]

    elif selected_filter == "only_totvs":
        employees_list = [
            employee for employee in employees_list
            if not employee.management_status
        ]

    paginator = Paginator(employees_list, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "selected_filter": selected_filter,
        "search": search,
        "total_employees": Employee.objects.filter(is_active=True).count(),
        "total_store_divergences": len([
            employee for employee in Employee.objects.filter(is_active=True).select_related("store")
            if employee.has_store_divergence()
        ]),
        "total_status_divergences": len([
            employee for employee in Employee.objects.filter(is_active=True)
            if employee.has_status_divergence()
        ]),
        "total_management_duplicates": len([
            employee for employee in Employee.objects.filter(is_active=True)
            if employee.has_management_duplicate_records()
        ]),
        "total_only_totvs": Employee.objects.filter(
            is_active=True,
            management_status__isnull=True,
        ).count() + Employee.objects.filter(
            is_active=True,
            management_status="",
        ).count(),
    }

    return render(request, "employees/employees_list.html", context)