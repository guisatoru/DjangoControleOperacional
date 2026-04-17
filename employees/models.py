import re
from django.db import models
from core.utils.normalizers import normalize_column_name


class Employee(models.Model):
    def has_management_duplicate_records(self):
        return self.management_non_transferred_records_count > 1

    def has_store_divergence(self):
        if not self.store or not self.management_store_name:
            return False

        system_store_name = normalize_column_name(self.store.name)
        management_store_name = normalize_column_name(self.management_store_name)

        if self.is_dia_consolidated_exception(management_store_name):
            return False

        if self.is_support_mobile_team_exception(system_store_name, management_store_name):
            return False

        return system_store_name != management_store_name


    def is_dia_consolidated_exception(self, management_store_name):
        if self.cost_center != "3476811":
            return False

        return re.search(r"\bDIA\b", management_store_name) is not None


    def is_support_mobile_team_exception(self, system_store_name, management_store_name):
        system_has_support = re.search(r"\bAPOIO\b", system_store_name) is not None
        system_has_mobile_team = re.search(r"\bVOLANTE\b", system_store_name) is not None

        management_has_support = re.search(r"\bAPOIO\b", management_store_name) is not None
        management_has_mobile_team = re.search(r"\bVOLANTE\b", management_store_name) is not None

        system_is_support_or_mobile = system_has_support or system_has_mobile_team
        management_is_support_or_mobile = management_has_support or management_has_mobile_team

        return system_is_support_or_mobile and management_is_support_or_mobile

    def has_status_divergence(self):
        management_status = normalize_column_name(self.management_status)
        payroll_status = normalize_column_name(self.payroll_status)

        if not management_status:
            return False

        if payroll_status == "D":
            return management_status != "DEMITIDO"

        if payroll_status == "F":
            return management_status != "FERIAS"

        if payroll_status == "A":
            return management_status != "AFASTADO"

        if payroll_status == "":
            return management_status in ["DEMITIDO", "FERIAS", "AFASTADO"]

        return False
    
    employee_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)

    store = models.ForeignKey(
        "stores.Store",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employees"
    )

    totvs_store_name = models.CharField(max_length=255, blank=True, null=True)
    cost_center = models.CharField(max_length=50, blank=True, null=True)

    totvs_job_title = models.CharField(max_length=255, blank=True, null=True)
    payroll_status = models.CharField(max_length=20, blank=True, null=True)

    admission_date = models.DateField(blank=True, null=True)
    first_contract_end_date = models.DateField(blank=True, null=True)
    second_contract_end_date = models.DateField(blank=True, null=True)
    dismissal_date = models.DateField(blank=True, null=True)

    management_store_name = models.CharField(max_length=255, blank=True, null=True)
    management_job_title = models.CharField(max_length=255, blank=True, null=True)
    management_status = models.CharField(max_length=50, blank=True, null=True)

    management_records_count = models.PositiveIntegerField(default=0)
    management_non_transferred_records_count = models.PositiveIntegerField(default=0)
    management_non_transferred_statuses = models.JSONField(default=list, blank=True)

    geo_store_name = models.CharField(max_length=255, blank=True, null=True)
    geo_user_id = models.CharField(max_length=100, blank=True, null=True)

    supervisor = models.CharField(max_length=255, blank=True, null=True)

    is_active = models.BooleanField(default=True)

    counts_in_store_headcount = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.employee_code} - {self.name}"