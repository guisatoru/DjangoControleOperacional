from rest_framework import serializers

from employees.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    store_id = serializers.SerializerMethodField()
    store_name = serializers.SerializerMethodField()
    supervisor = serializers.SerializerMethodField()
    has_store_divergence = serializers.SerializerMethodField()
    has_status_divergence = serializers.SerializerMethodField()
    has_management_duplicate_records = serializers.SerializerMethodField()
    has_management_data = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = [
            "id",
            "employee_code",
            "name",

            "store_id",
            "store_name",
            "cost_center",
            "supervisor",

            "management_store_name",
            "geo_store_name",
            "geo_user_id",

            "totvs_job_title",
            "management_job_title",

            "payroll_status",
            "management_status",

            "admission_date",
            "first_contract_end_date",
            "second_contract_end_date",
            "dismissal_date",

            "management_records_count",
            "management_non_transferred_records_count",
            "management_non_transferred_statuses",

            "is_active",
            "counts_in_store_headcount",

            "has_store_divergence",
            "has_status_divergence",
            "has_management_duplicate_records",
            "has_management_data",
        ]

    def get_store_name(self, employee):
        if employee.store:
            return employee.store.name

        return None
    
    def get_store_id(self, employee):
        if employee.store:
            return employee.store.id

        return None
    
    def get_supervisor(self, employee):
        if employee.store:
            return employee.store.supervisor

        return None

    def get_has_store_divergence(self, employee):
        return employee.has_store_divergence()

    def get_has_status_divergence(self, employee):
        return employee.has_status_divergence()

    def get_has_management_duplicate_records(self, employee):
        return employee.has_management_duplicate_records()

    def get_has_management_data(self, employee):
        return bool(employee.management_status)
