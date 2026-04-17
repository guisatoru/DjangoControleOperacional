import pandas as pd

from core.utils.normalizers import (
    normalize_employee_code,
    normalize_cost_center,
    normalize_text,
    normalize_column_name,
    parse_date,
)

IGNORED_COST_CENTERS = {
    "999999990010",
    "999999990050",
    "999999990020",
}

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


def parse_totvs_file(file_path):
    dataframe = pd.read_csv(
        file_path,
        sep=";",
        dtype=str,
        encoding="utf-8-sig",
        skiprows=2,
    )

    dataframe = normalize_dataframe_columns(dataframe)

    employees = []

    for _, row in dataframe.iterrows():
        employee_code = normalize_employee_code(
            get_value(row, ["MATRICULA"])
        )

        if not employee_code:
            continue

        cost_center = normalize_cost_center(
            get_value(row, ["C.C. MOVTO"])
        )

        if cost_center in IGNORED_COST_CENTERS:
            continue

        payroll_status = normalize_text(
            get_value(row, ["SIT. FOLHA"])
        ).upper()

        employee_data = {
            "employee_code": employee_code,
            "name": normalize_text(
                get_value(row, ["NOME COMPLET"])
            ),
            "cost_center": cost_center,
            "totvs_job_title": normalize_text(
                get_value(row, ["DESC.FUNCAO"])
            ),
            "payroll_status": payroll_status,
            "admission_date": parse_date(
                get_value(row, ["DATA ADMIS."])
            ),
            "first_contract_end_date": parse_date(
                get_value(row, ["VEN. EXPER.1"])
            ),
            "second_contract_end_date": parse_date(
                get_value(row, ["VC.EXP.2PER."])
            ),
            "dismissal_date": parse_date(
                get_value(row, ["DT. DEMISSAO"])
            ),
            "is_active": payroll_status != "D",
            "counts_in_store_headcount": payroll_status not in ["D", "A"],
        }

        employees.append(employee_data)

    return employees