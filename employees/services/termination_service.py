from django.core.paginator import Paginator
from django.db.models import Prefetch, Q
from django.utils import timezone

from core.utils.normalizers import normalize_column_name
from employees.models import Employee, TerminationControl


TERMINATIONS_PER_PAGE = 12
TERMINATION_ACTION_LABELS = {
    "prorrogado": "Prorrogado",
    "termino": "Termino registrado",
    "manter": "Mantido",
}
FORCED_STORE_COORDINATORS = {
    "DIA BRASIL SOCIEDADE LIMITADA": "EDGAR PAVAN",
}
TERMINATION_CACHE_FIELDS = [
    "termination_in_scope_cached",
    "termination_current_stage_cached",
    "termination_status_cached",
    "termination_type_cached",
    "termination_reference_date_cached",
    "termination_coordinator_cached",
    "termination_has_history_cached",
    "termination_closed_cached",
]


def normalize_status_for_termination(status_value):
    normalized = normalize_column_name(status_value)
    return normalized


def has_date_passed(date_value, reference_date):
    if not date_value:
        return False

    return date_value < reference_date


def is_excluded_by_management(employee):
    management_status = normalize_status_for_termination(employee.management_status)
    return "DEMIT" in management_status or "AFAST" in management_status


def get_latest_entry(entries, stage):
    stage_entries = [entry for entry in entries if entry.stage == stage]

    if not stage_entries:
        return None

    return sorted(
        stage_entries,
        key=lambda entry: entry.responded_at or entry.created_at,
        reverse=True,
    )[0]


def derive_termination_state(entries, employee, reference_date):
    latest_first = get_latest_entry(entries, 1)
    latest_second = get_latest_entry(entries, 2)
    first_term_passed = has_date_passed(employee.first_contract_end_date, reference_date)

    if latest_second and latest_second.action == "termino":
        return {
            "current_stage": 2,
            "termination_type": "2o Termino",
            "control_status": "Termino registrado",
            "closed": True,
        }

    if latest_second and latest_second.action == "manter":
        return {
            "current_stage": 2,
            "termination_type": "2o Termino",
            "control_status": "Mantido",
            "closed": True,
        }

    if latest_first and latest_first.action == "termino":
        return {
            "current_stage": 1,
            "termination_type": "1o Termino",
            "control_status": "Termino registrado",
            "closed": True,
        }

    if latest_first and latest_first.action == "prorrogado":
        return {
            "current_stage": 2,
            "termination_type": "2o Termino",
            "control_status": "Prorrogado",
            "closed": False,
        }

    if first_term_passed:
        return {
            "current_stage": 2,
            "termination_type": "2o Termino",
            "control_status": "Pendente 2o Termino",
            "closed": False,
        }

    return {
        "current_stage": 1,
        "termination_type": "1o Termino",
        "control_status": "Pendente 1o Termino",
        "closed": False,
    }


def build_history_item(entry):
    return {
        "id": entry.id,
        "stage": entry.stage,
        "action": entry.action,
        "action_label": TERMINATION_ACTION_LABELS.get(entry.action, entry.action),
        "observation": entry.observation,
        "responded_by": entry.responded_by or "Usuario",
        "responded_at": entry.responded_at,
        "created_at": entry.created_at,
    }


def get_available_actions(current_stage, closed):
    if closed:
        return []

    if current_stage == 1:
        return [
            {"value": "prorrogado", "label": "Prorrogar"},
            {"value": "termino", "label": "Dar termino"},
        ]

    return [
        {"value": "manter", "label": "Manter"},
        {"value": "termino", "label": "Dar termino"},
    ]


def get_store_coordinator(store):
    if not store:
        return ""

    forced_coordinator = FORCED_STORE_COORDINATORS.get((store.name or "").strip().upper())
    if forced_coordinator:
        return forced_coordinator

    return store.coordinator or ""


def build_termination_row(employee, entries, reference_date):
    state = derive_termination_state(entries, employee, reference_date)
    store = employee.store
    has_termination_history = any(entry.action == "termino" for entry in entries)
    sorted_entries = sorted(
        entries,
        key=lambda item: item.responded_at or item.created_at,
        reverse=True,
    )

    return {
        "id": employee.id,
        "employee_id": employee.id,
        "employee_code": employee.employee_code,
        "name": employee.name,
        "store_name": store.name if store else "",
        "state": store.state if store else "",
        "coordinator": get_store_coordinator(store),
        "admission_date": employee.admission_date,
        "first_contract_end_date": employee.first_contract_end_date,
        "second_contract_end_date": employee.second_contract_end_date,
        "management_status": employee.management_status,
        "payroll_status": employee.payroll_status,
        "totvs_job_title": employee.totvs_job_title,
        "management_job_title": employee.management_job_title,
        "geo_job_title": employee.geo_job_title,
        "management_store_name": employee.management_store_name,
        "geo_store_name": employee.geo_store_name,
        "geo_user_id": employee.geo_user_id,
        "current_stage": state["current_stage"],
        "termination_type": state["termination_type"],
        "control_status": state["control_status"],
        "closed": state["closed"],
        "history": [build_history_item(entry) for entry in sorted_entries],
        "keep_for_history": has_termination_history,
        "excluded_by_management": is_excluded_by_management(employee),
        "available_actions": get_available_actions(state["current_stage"], state["closed"]),
    }


def apply_termination_cache_fields(employee, entries, reference_date):
    row = build_termination_row(employee, entries, reference_date)

    employee.termination_in_scope_cached = should_include_termination_row(row, reference_date)
    employee.termination_current_stage_cached = row["current_stage"]
    employee.termination_status_cached = row["control_status"]
    employee.termination_type_cached = row["termination_type"]
    employee.termination_reference_date_cached = (
        row["second_contract_end_date"]
        if row["current_stage"] == 2 and row["second_contract_end_date"]
        else row["first_contract_end_date"]
    )
    employee.termination_coordinator_cached = row["coordinator"] or None
    employee.termination_has_history_cached = bool(row["history"])
    employee.termination_closed_cached = row["closed"]


def refresh_termination_cache_fields():
    employees = list(
        Employee.objects.select_related("store").prefetch_related(
            Prefetch(
                "termination_controls",
                queryset=TerminationControl.objects.order_by("-responded_at", "-created_at"),
            )
        )
    )
    reference_date = timezone.localdate()
    employees_to_update = []

    for employee in employees:
        previous_values = {
            field_name: getattr(employee, field_name)
            for field_name in TERMINATION_CACHE_FIELDS
        }
        entries = list(employee.termination_controls.all())
        apply_termination_cache_fields(employee, entries, reference_date)

        has_changes = any(
            getattr(employee, field_name) != previous_values[field_name]
            for field_name in TERMINATION_CACHE_FIELDS
        )

        if has_changes:
            employees_to_update.append(employee)

    if employees_to_update:
        Employee.objects.bulk_update(
            employees_to_update,
            TERMINATION_CACHE_FIELDS,
            batch_size=500,
        )


def refresh_single_employee_termination_cache(employee):
    reference_date = timezone.localdate()
    entries = list(employee.termination_controls.all())
    apply_termination_cache_fields(employee, entries, reference_date)
    Employee.objects.filter(id=employee.id).update(
        termination_in_scope_cached=employee.termination_in_scope_cached,
        termination_current_stage_cached=employee.termination_current_stage_cached,
        termination_status_cached=employee.termination_status_cached,
        termination_type_cached=employee.termination_type_cached,
        termination_reference_date_cached=employee.termination_reference_date_cached,
        termination_coordinator_cached=employee.termination_coordinator_cached,
        termination_has_history_cached=employee.termination_has_history_cached,
        termination_closed_cached=employee.termination_closed_cached,
    )


def should_include_termination_row(row, reference_date):
    if row["excluded_by_management"] and not row["keep_for_history"]:
        return False

    if not row["admission_date"]:
        return False

    if not (row["first_contract_end_date"] or row["second_contract_end_date"]):
        return False

    if (
        has_date_passed(row["first_contract_end_date"], reference_date)
        and has_date_passed(row["second_contract_end_date"], reference_date)
        and len(row["history"]) == 0
    ):
        return False

    return True


def get_termination_employees_queryset():
    return (
        Employee.objects.select_related("store")
        .prefetch_related(
            Prefetch(
                "termination_controls",
                queryset=TerminationControl.objects.order_by("-responded_at", "-created_at"),
            )
        )
        .filter(termination_in_scope_cached=True)
    )


def build_termination_rows(employees):
    rows = []

    for employee in employees:
        entries = list(employee.termination_controls.all())
        row = build_termination_row(employee, entries, timezone.localdate())
        rows.append(row)

    return sorted(
        rows,
        key=lambda row: (
            row["admission_date"] or timezone.localdate(),
            row["name"] or "",
        ),
    )


def get_base_termination_rows():
    employees = list(get_termination_employees_queryset())
    return build_termination_rows(employees)


def get_base_termination_queryset():
    return Employee.objects.select_related("store").filter(termination_in_scope_cached=True)


def apply_scope_filters(rows, search="", date_from="", coordinator="all"):
    filtered_rows = rows

    normalized_search = (search or "").strip().lower()
    if normalized_search:
        filtered_rows = [
            row
            for row in filtered_rows
            if normalized_search in (row["name"] or "").lower()
            or normalized_search in (row["employee_code"] or "").lower()
        ]

    if coordinator and coordinator != "all":
        filtered_rows = [
            row
            for row in filtered_rows
            if (row["coordinator"] or "") == coordinator
        ]

    if date_from:
        filtered_rows = [
            row
            for row in filtered_rows
            if (
                row["second_contract_end_date"]
                if row["current_stage"] == 2 and row["second_contract_end_date"]
                else row["first_contract_end_date"]
            )
            and (
                (row["second_contract_end_date"] if row["current_stage"] == 2 and row["second_contract_end_date"] else row["first_contract_end_date"]).isoformat()
                >= date_from
            )
        ]

    return filtered_rows


def apply_scope_filters_to_queryset(queryset, search="", date_from="", coordinator="all"):
    filtered_queryset = queryset

    normalized_search = (search or "").strip()
    if normalized_search:
        filtered_queryset = filtered_queryset.filter(
            Q(name__icontains=normalized_search)
            | Q(employee_code__icontains=normalized_search)
        )

    if coordinator and coordinator != "all":
        filtered_queryset = filtered_queryset.filter(
            termination_coordinator_cached=coordinator
        )

    if date_from:
        filtered_queryset = filtered_queryset.filter(
            termination_reference_date_cached__gte=date_from
        )

    return filtered_queryset


def apply_termination_status_filter(rows, selected_filter="all"):
    filtered_rows = rows

    if selected_filter != "all":
        filter_map = {
            "pending_first": "Pendente 1o Termino",
            "pending_second": "Pendente 2o Termino",
            "prorrogado": "Prorrogado",
            "mantido": "Mantido",
            "terminated": "Termino registrado",
        }
        expected_status = filter_map.get(selected_filter)
        if expected_status:
            filtered_rows = [
                row
                for row in filtered_rows
                if row["control_status"] == expected_status
            ]

    return filtered_rows


def build_termination_summary(rows):
    return {
        "total_terminations": len(rows),
        "total_pending_first": sum(1 for row in rows if row["control_status"] == "Pendente 1o Termino"),
        "total_pending_second": sum(1 for row in rows if row["control_status"] == "Pendente 2o Termino"),
        "total_prorrogado": sum(1 for row in rows if row["control_status"] == "Prorrogado"),
        "total_mantido": sum(1 for row in rows if row["control_status"] == "Mantido"),
        "total_terminated": sum(1 for row in rows if row["control_status"] == "Termino registrado"),
    }


def get_coordinator_options(rows):
    coordinators = sorted({row["coordinator"] for row in rows if row["coordinator"]})
    return coordinators


def build_termination_summary_from_queryset(queryset):
    return {
        "total_terminations": queryset.count(),
        "total_pending_first": queryset.filter(termination_status_cached="Pendente 1o Termino").count(),
        "total_pending_second": queryset.filter(termination_status_cached="Pendente 2o Termino").count(),
        "total_prorrogado": queryset.filter(termination_status_cached="Prorrogado").count(),
        "total_mantido": queryset.filter(termination_status_cached="Mantido").count(),
        "total_terminated": queryset.filter(termination_status_cached="Termino registrado").count(),
    }


def get_coordinator_options_from_queryset(queryset):
    return sorted(
        {
            coordinator
            for coordinator in queryset.values_list("termination_coordinator_cached", flat=True)
            if coordinator
        }
    )


def paginate_terminations(selected_filter="all", search="", page_number=1, date_from="", coordinator="all"):
    base_queryset = get_base_termination_queryset()
    scoped_queryset = apply_scope_filters_to_queryset(
        base_queryset,
        search=search,
        date_from=date_from,
        coordinator=coordinator,
    )

    status_map = {
        "pending_first": "Pendente 1o Termino",
        "pending_second": "Pendente 2o Termino",
        "prorrogado": "Prorrogado",
        "mantido": "Mantido",
        "terminated": "Termino registrado",
    }
    filtered_queryset = scoped_queryset
    expected_status = status_map.get(selected_filter)
    if expected_status:
        filtered_queryset = filtered_queryset.filter(termination_status_cached=expected_status)

    paginator = Paginator(filtered_queryset.order_by("admission_date", "name"), TERMINATIONS_PER_PAGE)
    page_obj = paginator.get_page(page_number)
    results = build_termination_rows(list(page_obj.object_list.prefetch_related(
        Prefetch(
            "termination_controls",
            queryset=TerminationControl.objects.order_by("-responded_at", "-created_at"),
        )
    )))

    return {
        "page_obj": page_obj,
        "results": results,
        "summary": build_termination_summary_from_queryset(scoped_queryset),
        "coordinators": get_coordinator_options_from_queryset(scoped_queryset),
    }


def get_termination_detail(employee_id):
    try:
        employee = get_termination_employees_queryset().get(id=employee_id)
    except Employee.DoesNotExist:
        return None

    rows = build_termination_rows([employee])
    return rows[0] if rows else None


def create_termination_control(employee_id, stage, action, observation, responded_by="Usuario"):
    employee = Employee.objects.select_related("store").prefetch_related(
        Prefetch(
            "termination_controls",
            queryset=TerminationControl.objects.order_by("-responded_at", "-created_at"),
        )
    ).get(id=employee_id)
    responded_at = timezone.now()

    control = TerminationControl.objects.create(
        employee=employee,
        employee_code=employee.employee_code,
        stage=stage,
        action=action,
        observation=observation,
        responded_by=responded_by or "Usuario",
        responded_at=responded_at,
    )
    employee = Employee.objects.select_related("store").prefetch_related(
        Prefetch(
            "termination_controls",
            queryset=TerminationControl.objects.order_by("-responded_at", "-created_at"),
        )
    ).get(id=employee_id)
    refresh_single_employee_termination_cache(employee)
    return control
