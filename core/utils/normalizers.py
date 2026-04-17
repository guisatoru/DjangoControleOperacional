import re
import unicodedata
from datetime import datetime, date

def normalize_column_name(value):
    if value is None:
        return ""

    value = str(value).strip().upper()

    value = unicodedata.normalize("NFKD", value)
    value = "".join(char for char in value if not unicodedata.combining(char))

    return " ".join(value.split())

def normalize_digits(value):
    if value is None:
        return ""

    value = str(value).strip()
    return re.sub(r"\D", "", value)


def normalize_employee_code(value):
    digits = normalize_digits(value)

    if not digits:
        return ""

    return digits.lstrip("0") or "0"


def normalize_cost_center(value):
    digits = normalize_digits(value)

    if not digits:
        return ""

    return digits.lstrip("0") or "0"


def normalize_text(value):
    if value is None:
        return ""

    return str(value).strip()


def parse_date(value):
    if value is None or value == "":
        return None

    if isinstance(value, date):
        return value

    value = str(value).strip()

    formats = [
        "%d/%m/%Y",
        "%Y-%m-%d",
        "%d-%m-%Y",
    ]

    for date_format in formats:
        try:
            return datetime.strptime(value, date_format).date()
        except ValueError:
            pass

    return None