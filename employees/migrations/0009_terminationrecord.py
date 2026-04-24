from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("employees", "0008_dismissalrecord_totvs_dates"),
    ]

    operations = [
        migrations.CreateModel(
            name="TerminationRecord",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("employee_code", models.CharField(max_length=20, unique=True)),
                ("name", models.CharField(max_length=255)),
                ("admission_date", models.DateField(blank=True, null=True)),
                ("first_contract_end_date", models.DateField(blank=True, null=True)),
                ("second_contract_end_date", models.DateField(blank=True, null=True)),
                ("reference_end_date", models.DateField(blank=True, null=True)),
                ("current_stage", models.CharField(blank=True, max_length=20, null=True)),
                ("attention_status", models.CharField(default="future", max_length=20)),
                ("payroll_status", models.CharField(blank=True, max_length=20, null=True)),
                ("management_status", models.CharField(blank=True, max_length=50, null=True)),
                ("store_name", models.CharField(blank=True, max_length=255, null=True)),
                ("management_store_name", models.CharField(blank=True, max_length=255, null=True)),
                ("geo_store_name", models.CharField(blank=True, max_length=255, null=True)),
                ("totvs_job_title", models.CharField(blank=True, max_length=255, null=True)),
                ("management_job_title", models.CharField(blank=True, max_length=255, null=True)),
                ("geo_job_title", models.CharField(blank=True, max_length=255, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "employee",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="termination_record",
                        to="employees.employee",
                    ),
                ),
            ],
            options={
                "ordering": ["reference_end_date", "name"],
            },
        ),
    ]
