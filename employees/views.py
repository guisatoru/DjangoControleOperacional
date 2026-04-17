from django.shortcuts import render

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