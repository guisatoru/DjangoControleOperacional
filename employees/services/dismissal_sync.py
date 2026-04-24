from core.utils.normalizers import normalize_column_name
from employees.models import DismissalRecord, Employee


DISMISSAL_UPDATE_FIELDS = [
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


def build_dismissal_comparison_status(employee):
    management_status = normalize_column_name(employee.management_status)

    if not management_status:
        return "pending"

    if management_status == "DEMITIDO":
        return "ok"

    return "divergent"


def build_dismissal_values(employee):
    return {
        "employee_code": employee.employee_code,
        "name": employee.name,
        "admission_date": employee.admission_date,
        "dismissal_date": employee.dismissal_date,
        "first_contract_end_date": employee.first_contract_end_date,
        "second_contract_end_date": employee.second_contract_end_date,
        "payroll_status": employee.payroll_status,
        "management_status": employee.management_status,
        "store_name": employee.store.name if employee.store else None,
        "management_store_name": employee.management_store_name,
        "geo_store_name": employee.geo_store_name,
        "totvs_job_title": employee.totvs_job_title,
        "management_job_title": employee.management_job_title,
        "geo_job_title": employee.geo_job_title,
        "comparison_status": build_dismissal_comparison_status(employee),
    }


def apply_field_values(instance, field_values):
    has_changes = False

    for field_name, new_value in field_values.items():
        if getattr(instance, field_name) != new_value:
            setattr(instance, field_name, new_value)
            has_changes = True

    return has_changes


def sync_dismissal_records():
    employees = list(Employee.objects.select_related("store").all())
    dismissed_employees = [employee for employee in employees if employee.is_dismissed()]
    dismissed_employee_ids = {employee.id for employee in dismissed_employees}

    existing_records = {
        record.employee_id: record
        for record in DismissalRecord.objects.select_related("employee").all()
    }

    records_to_create = []
    records_to_update = []

    for employee in dismissed_employees:
        field_values = build_dismissal_values(employee)
        existing_record = existing_records.get(employee.id)

        if not existing_record:
            records_to_create.append(DismissalRecord(employee=employee, **field_values))
            continue

        if apply_field_values(existing_record, field_values):
            records_to_update.append(existing_record)

    stale_record_ids = [
        record.id
        for employee_id, record in existing_records.items()
        if employee_id not in dismissed_employee_ids
    ]

    if records_to_create:
        DismissalRecord.objects.bulk_create(records_to_create)

    if records_to_update:
        DismissalRecord.objects.bulk_update(records_to_update, DISMISSAL_UPDATE_FIELDS, batch_size=500)

    if stale_record_ids:
        DismissalRecord.objects.filter(id__in=stale_record_ids).delete()
