from django.db import models


class Employee(models.Model):
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

    geo_store_name = models.CharField(max_length=255, blank=True, null=True)
    geo_user_id = models.CharField(max_length=100, blank=True, null=True)

    supervisor = models.CharField(max_length=255, blank=True, null=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.employee_code} - {self.name}"