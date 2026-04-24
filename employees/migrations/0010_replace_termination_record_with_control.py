from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("employees", "0009_terminationrecord"),
    ]

    operations = [
        migrations.DeleteModel(
            name="TerminationRecord",
        ),
        migrations.CreateModel(
            name="TerminationControl",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("employee_code", models.CharField(max_length=20)),
                ("stage", models.PositiveSmallIntegerField()),
                ("action", models.CharField(max_length=20)),
                ("observation", models.TextField()),
                ("responded_by", models.CharField(blank=True, max_length=255, null=True)),
                ("responded_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="termination_controls",
                        to="employees.employee",
                    ),
                ),
            ],
            options={
                "ordering": ["-responded_at", "-created_at"],
            },
        ),
    ]
