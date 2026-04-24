import re
from django.db import models
from core.utils.normalizers import normalize_column_name, normalize_job_title_for_comparison


class Employee(models.Model):
    def has_management_duplicate_records(self):
        return self.management_non_transferred_records_count > 1

    def is_dismissed(self):
        payroll_status = normalize_column_name(self.payroll_status)
        management_status = normalize_column_name(self.management_status)

        return (
            payroll_status == "D"
            or management_status == "DEMITIDO"
            or self.dismissal_date is not None
        )

    def has_store_divergence(self):
        store_names = self.get_store_names_for_comparison()

        if len(store_names) < 2:
            return False

        if self.is_dia_consolidated_exception(store_names):
            return False

        if self.is_support_mobile_team_exception(store_names):
            return False

        return len(set(store_names.values())) > 1


    def get_store_names_for_comparison(self):
        store_names = {}

        if self.store and self.store.name:
            store_names["totvs"] = normalize_column_name(self.store.name)

        if self.management_store_name:
            store_names["management"] = normalize_column_name(self.management_store_name)

        if self.geo_store_name:
            store_names["geo"] = normalize_column_name(self.geo_store_name)

        return {
            source_name: store_name
            for source_name, store_name in store_names.items()
            if store_name
        }


    def is_dia_consolidated_exception(self, store_names):
        if self.cost_center != "3476811":
            return False

        return any(re.search(r"\bDIA\b", store_name) is not None for store_name in store_names.values())


    def is_support_mobile_team_exception(self, store_names):
        if len(store_names) < 2:
            return False

        return all(self.is_support_or_mobile_store_name(store_name) for store_name in store_names.values())


    def is_support_or_mobile_store_name(self, store_name):
        has_support = re.search(r"\bAPOIO\b", store_name) is not None
        has_mobile_team = re.search(r"\bVOLANTE\b", store_name) is not None
        return has_support or has_mobile_team

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


    def has_job_title_divergence(self):
        job_titles = []

        if self.totvs_job_title:
            job_titles.append(normalize_job_title_for_comparison(self.totvs_job_title))

        if self.management_job_title:
            job_titles.append(normalize_job_title_for_comparison(self.management_job_title))

        if self.geo_job_title:
            job_titles.append(normalize_job_title_for_comparison(self.geo_job_title))

        normalized_job_titles = [job_title for job_title in job_titles if job_title]

        if len(normalized_job_titles) < 2:
            return False

        return len(set(normalized_job_titles)) > 1
    
    employee_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)

    store = models.ForeignKey(
        "stores.Store",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employees"
    )

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
    geo_cost_center_code = models.CharField(max_length=50, blank=True, null=True)
    geo_job_title = models.CharField(max_length=255, blank=True, null=True)
    geo_user_id = models.CharField(max_length=100, blank=True, null=True)

    supervisor = models.CharField(max_length=255, blank=True, null=True)

    is_active = models.BooleanField(default=True)

    counts_in_store_headcount = models.BooleanField(default=True)
    has_store_divergence_cached = models.BooleanField(default=False)
    has_job_title_divergence_cached = models.BooleanField(default=False)
    has_status_divergence_cached = models.BooleanField(default=False)
    has_management_duplicate_cached = models.BooleanField(default=False)
    has_management_data_cached = models.BooleanField(default=False)
    termination_in_scope_cached = models.BooleanField(default=False)
    termination_current_stage_cached = models.PositiveSmallIntegerField(blank=True, null=True)
    termination_status_cached = models.CharField(max_length=50, blank=True, null=True)
    termination_type_cached = models.CharField(max_length=30, blank=True, null=True)
    termination_reference_date_cached = models.DateField(blank=True, null=True)
    termination_coordinator_cached = models.CharField(max_length=255, blank=True, null=True)
    termination_has_history_cached = models.BooleanField(default=False)
    termination_closed_cached = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.employee_code} - {self.name}"


class DismissalRecord(models.Model):
    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        related_name="dismissal_record",
    )
    employee_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    admission_date = models.DateField(blank=True, null=True)
    dismissal_date = models.DateField(blank=True, null=True)
    first_contract_end_date = models.DateField(blank=True, null=True)
    second_contract_end_date = models.DateField(blank=True, null=True)
    payroll_status = models.CharField(max_length=20, blank=True, null=True)
    management_status = models.CharField(max_length=50, blank=True, null=True)
    store_name = models.CharField(max_length=255, blank=True, null=True)
    management_store_name = models.CharField(max_length=255, blank=True, null=True)
    geo_store_name = models.CharField(max_length=255, blank=True, null=True)
    totvs_job_title = models.CharField(max_length=255, blank=True, null=True)
    management_job_title = models.CharField(max_length=255, blank=True, null=True)
    geo_job_title = models.CharField(max_length=255, blank=True, null=True)
    comparison_status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-dismissal_date", "name"]

    def __str__(self):
        return f"{self.employee_code} - {self.name}"


class TerminationControl(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="termination_controls",
    )
    employee_code = models.CharField(max_length=20)
    stage = models.PositiveSmallIntegerField()
    action = models.CharField(max_length=20)
    observation = models.TextField()
    responded_by = models.CharField(max_length=255, blank=True, null=True)
    responded_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-responded_at", "-created_at"]

    def __str__(self):
        return f"{self.employee_code} - etapa {self.stage} - {self.action}"
