from rest_framework import serializers

from employees.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    store_id = serializers.SerializerMethodField()
    store_name = serializers.SerializerMethodField()
    supervisor = serializers.SerializerMethodField()
    has_store_divergence = serializers.BooleanField(source="has_store_divergence_cached", read_only=True)
    has_job_title_divergence = serializers.BooleanField(source="has_job_title_divergence_cached", read_only=True)
    has_status_divergence = serializers.BooleanField(source="has_status_divergence_cached", read_only=True)
    has_management_duplicate_records = serializers.BooleanField(source="has_management_duplicate_cached", read_only=True)
    has_management_data = serializers.BooleanField(source="has_management_data_cached", read_only=True)

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
            "geo_cost_center_code",
            "geo_job_title",
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
            "has_job_title_divergence",
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

