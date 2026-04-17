from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        "employee_code",
        "name",
        "cost_center",
        "payroll_status",
        "store",
        "management_store_name",
        "management_job_title",
        "management_status",
        "is_active",
    ]

    search_fields = [
        "employee_code",
        "name",
        "cost_center",
        "management_store_name",
        "management_job_title",
    ]

    list_filter = [
        "is_active",
        "payroll_status",
        "management_status",
        "store",
    ]

    readonly_fields = [
        "created_at",
        "updated_at",
    ]