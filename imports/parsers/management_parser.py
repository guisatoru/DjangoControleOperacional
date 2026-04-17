import pandas as pd

from core.utils.normalizers import (
    normalize_column_name,
    normalize_employee_code,
    normalize_text,
)


def normalize_dataframe_columns(dataframe):
    dataframe = dataframe.copy()
    dataframe.columns = [normalize_column_name(column) for column in dataframe.columns]
    return dataframe


def get_value(row, possible_columns):
    normalized_columns = [normalize_column_name(column) for column in possible_columns]

    for column in normalized_columns:
        if column in row and pd.notna(row[column]):
            return row[column]

    return None


def normalize_dash(value):
    value = normalize_text(value)

    if value == "-":
        return ""

    return value


def parse_management_employees_file(file_path):
    dataframe = pd.read_excel(
        file_path,
        sheet_name="Relação de funcionários",
        dtype=str,
    )

    dataframe = normalize_dataframe_columns(dataframe)

    grouped_by_employee_code = {}

    for _, row in dataframe.iterrows():
        employee_code = normalize_employee_code(
            get_value(row, ["CÓD. FUNCIONÁRIO", "COD. FUNCIONARIO"])
        )

        if not employee_code:
            continue

        status = normalize_text(
            get_value(row, ["STATUS"])
        ).upper()

        employee_data = {
            "employee_code": employee_code,
            "management_job_title": normalize_text(
                get_value(row, ["FUNÇÃO", "FUNCAO"])
            ),
            "management_store_name": normalize_text(
                get_value(row, ["LOJA"])
            ),
            "management_status": status,
        }

        grouped_by_employee_code.setdefault(employee_code, [])
        grouped_by_employee_code[employee_code].append(employee_data)

    employees = []

    for employee_code, records in grouped_by_employee_code.items():
        non_transferred_records = [
            record for record in records
            if record["management_status"] != "TRANSFERIDO"
        ]

        if non_transferred_records:
            selected_record = non_transferred_records[-1]
        else:
            selected_record = records[-1]

        non_transferred_statuses = sorted({
            record["management_status"]
            for record in non_transferred_records
            if record["management_status"]
        })

        selected_record["management_records_count"] = len(records)
        selected_record["management_non_transferred_records_count"] = len(non_transferred_records)
        selected_record["management_non_transferred_statuses"] = non_transferred_statuses

        employees.append(selected_record)

    return employees


def parse_management_supervision_file(file_path):
    dataframe = pd.read_excel(
        file_path,
        sheet_name="mapeamento_supervisão",
        dtype=str,
    )

    dataframe = normalize_dataframe_columns(dataframe)

    stores = []

    for _, row in dataframe.iterrows():
        store_name = normalize_text(
            get_value(row, ["LOJA"])
        )

        if not store_name:
            continue

        supervisor = normalize_dash(
            get_value(row, ["SUPERVISÃO", "SUPERVISAO"])
        )

        regional_coordinator = normalize_dash(
            get_value(row, ["COORDENADOR REGIONAL"])
        )

        general_coordinator = normalize_dash(
            get_value(row, ["COORDENADOR GERAL"])
        )

        coordinator = regional_coordinator or general_coordinator

        store_data = {
            "store_name": store_name,
            "supervisor": supervisor,
            "coordinator": coordinator,
        }

        stores.append(store_data)

    return stores