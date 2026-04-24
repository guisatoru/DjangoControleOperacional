from rest_framework import serializers

from employees.models import DismissalRecord


class DismissalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DismissalRecord
        fields = [
            "id",
            "employee_code",
            "name",
            "admission_date",
            "dismissal_date",
            "first_contract_end_date",
            "second_contract_end_date",
            "payroll_status",
            "management_status",
            "store_name",
            "management_store_name",
            "geo_store_name",
            "totvs_job_title",
            "management_job_title",
            "geo_job_title",
            "comparison_status",
        ]
