from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employees", "0010_replace_termination_record_with_control"),
    ]

    operations = [
        migrations.AddField(
            model_name="employee",
            name="termination_closed_cached",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="employee",
            name="termination_coordinator_cached",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="employee",
            name="termination_current_stage_cached",
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="employee",
            name="termination_has_history_cached",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="employee",
            name="termination_in_scope_cached",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="employee",
            name="termination_reference_date_cached",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="employee",
            name="termination_status_cached",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="employee",
            name="termination_type_cached",
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
