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
        "is_active",
    ]

    search_fields = [
        "employee_code",
        "name",
        "cost_center",
        "totvs_store_name",
    ]

    list_filter = [
        "is_active",
        "payroll_status",
        "management_status",
    ]