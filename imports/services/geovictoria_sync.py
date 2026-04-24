import json
import time
from urllib import error, request

from django.conf import settings

from core.utils.normalizers import normalize_cost_center, normalize_employee_code, normalize_text
from employees.models import Employee
from stores.models import Store


GEO_EMPLOYEE_UPDATE_FIELDS = [
    "geo_user_id",
    "geo_job_title",
    "geo_cost_center_code",
    "geo_store_name",
]
TOKEN_TTL_SECONDS = 4 * 60 * 60
_TOKEN_CACHE = {
    "value": None,
    "fetched_at": 0,
}

def build_json_request(url, payload=None, token=None, method="POST", raw_authorization=False):
    headers = {
        "Accept": "application/json",
    }

    if token:
        headers["Authorization"] = token if raw_authorization else f"Bearer {token}"

    request_body = None

    if payload is not None:
        headers["Content-Type"] = "application/json"
        request_body = json.dumps(payload).encode("utf-8")

    return request.Request(
        url=url,
        data=request_body,
        headers=headers,
        method=method,
    )


def send_json_request(url, payload=None, token=None, method="POST", raw_authorization=False):
    http_request = build_json_request(
        url,
        payload=payload,
        token=token,
        method=method,
        raw_authorization=raw_authorization,
    )

    try:
        with request.urlopen(http_request, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        response_body = exc.read().decode("utf-8", errors="ignore")
        raise ValueError(f"GeoVictoria retornou erro HTTP {exc.code}: {response_body}") from exc
    except error.URLError as exc:
        raise ValueError(f"Nao foi possivel conectar ao GeoVictoria: {exc.reason}") from exc


def extract_bearer_token(login_response):
    possible_paths = [
        login_response.get("token"),
        login_response.get("data", {}).get("token") if isinstance(login_response.get("data"), dict) else None,
    ]

    for token in possible_paths:
        if token:
            return str(token)

    raise ValueError("Nao foi possivel encontrar o bearer token na resposta do login do GeoVictoria.")


def get_geovictoria_token():
    now = time.time()
    cached_token = _TOKEN_CACHE.get("value")
    cached_at = _TOKEN_CACHE.get("fetched_at", 0)

    if cached_token and (now - cached_at) < TOKEN_TTL_SECONDS:
        return cached_token

    if not settings.GEOVICTORIA_USER or not settings.GEOVICTORIA_PASSWORD:
        raise ValueError(
            "Defina GEOVICTORIA_USER e GEOVICTORIA_PASSWORD no arquivo .env antes de sincronizar."
        )

    login_payload = {
        "User": settings.GEOVICTORIA_USER,
        "Password": settings.GEOVICTORIA_PASSWORD,
    }
    login_response = send_json_request(settings.GEOVICTORIA_LOGIN_URL, login_payload)
    token = extract_bearer_token(login_response)
    _TOKEN_CACHE["value"] = token
    _TOKEN_CACHE["fetched_at"] = now
    return token


def fetch_geovictoria_users(token):
    response_data = send_json_request(
        settings.GEOVICTORIA_USER_LIST_URL,
        token=token,
        method="POST",
    )

    if isinstance(response_data, list):
        return response_data

    for key in ["data", "Data", "users", "Users", "result", "Result"]:
        value = response_data.get(key)
        if isinstance(value, list):
            return value

    raise ValueError("Nao foi possivel encontrar a lista de usuarios na resposta do GeoVictoria.")


def extract_timeoff_entries(timeoff_response):
    if isinstance(timeoff_response, list):
        return timeoff_response

    for key in ["data", "Data", "result", "Result", "TimeOff"]:
        value = timeoff_response.get(key)
        if isinstance(value, list):
            return value

    return []


def normalize_timeoff_description(value):
    return normalize_text(value)


def format_timeoff_date(value):
    raw_value = str(value or "").strip()
    digits_only = "".join(character for character in raw_value if character.isdigit())

    if len(digits_only) == 8:
        return f"{digits_only}000000"

    if len(digits_only) == 14:
        return digits_only

    raise ValueError("Data invalida para consulta de afastamentos na GeoVictoria.")


def parse_geovictoria_date(value):
    digits_only = "".join(character for character in str(value or "") if character.isdigit())

    if len(digits_only) < 8:
        return None

    year = int(digits_only[0:4])
    month = int(digits_only[4:6])
    day = int(digits_only[6:8])

    try:
        from datetime import date

        return date(year, month, day)
    except ValueError:
        return None


def get_inclusive_timeoff_days(entry):
    start_date = parse_geovictoria_date(entry.get("Starts"))
    end_date = parse_geovictoria_date(entry.get("Ends"))

    if not start_date or not end_date:
        return 1

    return max(1, (end_date - start_date).days + 1)


def get_geovictoria_timeoff_summary(start_date, end_date, user_id):
    if not user_id:
        raise ValueError("Identifier da GeoVictoria nao informado.")

    token = get_geovictoria_token()
    payload = {
        "StartDate": format_timeoff_date(start_date),
        "EndDate": format_timeoff_date(end_date),
        "UserIds": str(user_id),
    }

    try:
        timeoff_response = send_json_request(
            settings.GEOVICTORIA_TIMEOFF_URL,
            payload=payload,
            token=token,
            method="POST",
        )
    except ValueError:
        timeoff_response = send_json_request(
            settings.GEOVICTORIA_TIMEOFF_URL,
            payload=payload,
            token=token,
            method="POST",
            raw_authorization=True,
        )
    entries = extract_timeoff_entries(timeoff_response)

    medical_certificate_days = 0
    absences = 0

    for entry in entries:
        description = normalize_timeoff_description(entry.get("TimeOffTypeDescription"))
        total_days = get_inclusive_timeoff_days(entry)

        if description == "ATESTADO MEDICO":
            medical_certificate_days += total_days

        if description == "FALTA":
            absences += total_days

    return {
        "medical_certificate_days": medical_certificate_days,
        "absences": absences,
        "total_entries": len(entries),
    }


def get_geo_user_identifier(geo_user_data):
    for key in ["Identifier"]:
        value = geo_user_data.get(key)
        if value is not None and value != "":
            return str(value)

    return ""


def build_geovictoria_lookup(geo_users):
    users_by_employee_code = {}

    for geo_user in geo_users:
        employee_code = normalize_employee_code(geo_user.get("LastName"))

        if not employee_code:
            continue

        users_by_employee_code[employee_code] = {
            "geo_user_id": get_geo_user_identifier(geo_user),
            "geo_job_title": normalize_text(geo_user.get("PositionDescription")),
            "geo_cost_center_code": normalize_cost_center(geo_user.get("CostCenterCode")),
        }

    return users_by_employee_code


def apply_geo_data(employee, geo_data, stores_by_cost_center):
    geo_cost_center_code = geo_data.get("geo_cost_center_code", "")
    matched_store = stores_by_cost_center.get(geo_cost_center_code)
    next_values = {
        "geo_user_id": geo_data.get("geo_user_id") or None,
        "geo_job_title": geo_data.get("geo_job_title") or None,
        "geo_cost_center_code": geo_cost_center_code or None,
        "geo_store_name": matched_store.name if matched_store else None,
    }

    has_changes = False

    for field_name, new_value in next_values.items():
        if getattr(employee, field_name) != new_value:
            setattr(employee, field_name, new_value)
            has_changes = True

    return has_changes, matched_store is not None


def sync_geovictoria_data():
    token = get_geovictoria_token()
    geo_users = fetch_geovictoria_users(token)
    geo_users_by_employee_code = build_geovictoria_lookup(geo_users)

    employees = list(Employee.objects.all())
    stores_by_cost_center = {
        normalize_cost_center(store.cost_center): store
        for store in Store.objects.all()
    }

    summary = {
        "total_geo_records": len(geo_users),
        "total_unique_res": len(geo_users_by_employee_code),
        "total_employees": len(employees),
        "matched_employees": 0,
        "updated": 0,
        "unchanged": 0,
        "employee_not_found_in_geo": 0,
        "store_resolved": 0,
        "store_not_resolved": 0,
    }

    employees_to_update = []

    for employee in employees:
        geo_data = geo_users_by_employee_code.get(normalize_employee_code(employee.employee_code))

        if not geo_data:
            summary["employee_not_found_in_geo"] += 1
            continue

        summary["matched_employees"] += 1
        has_changes, store_resolved = apply_geo_data(employee, geo_data, stores_by_cost_center)

        if store_resolved:
            summary["store_resolved"] += 1
        else:
            summary["store_not_resolved"] += 1

        if has_changes:
            employees_to_update.append(employee)
            summary["updated"] += 1
        else:
            summary["unchanged"] += 1

    if employees_to_update:
        Employee.objects.bulk_update(employees_to_update, GEO_EMPLOYEE_UPDATE_FIELDS, batch_size=500)

    return summary
