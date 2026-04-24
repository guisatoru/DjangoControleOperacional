import re

import pandas as pd

from core.utils.normalizers import (
    normalize_column_name,
    normalize_cost_center,
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


def normalize_sheet_name(value):
    normalized_value = normalize_column_name(value)
    normalized_value = re.sub(r"[^A-Z0-9]+", " ", normalized_value)
    return " ".join(normalized_value.split())


def read_excel_sheet_by_alias(file_path, possible_sheet_names):
    normalized_possible_names = {
        normalize_sheet_name(name)
        for name in possible_sheet_names
    }

    with pd.ExcelFile(file_path) as workbook:
        for sheet_name in workbook.sheet_names:
            normalized_sheet_name = normalize_sheet_name(sheet_name)

            if normalized_sheet_name in normalized_possible_names:
                return pd.read_excel(workbook, sheet_name=sheet_name, dtype=str)

        available_sheet_names = ", ".join(workbook.sheet_names)

    raise ValueError(
        "Nao foi possivel localizar a aba da Tabela Mae. "
        f"Abas encontradas: {available_sheet_names}"
    )


def parse_mother_table_file(file_path):
    dataframe = read_excel_sheet_by_alias(
        file_path,
        ["MAE COM PROCS", "MÃE COM PROCS", "MAE_COM_PROCS"],
    )

    dataframe = normalize_dataframe_columns(dataframe)
    stores = []
    active_statuses = ["ATIVO", "FORA DA GESTAO"]

    for _, row in dataframe.iterrows():
        status = normalize_text(get_value(row, ["STATUS"])).upper()
        cost_center = normalize_cost_center(get_value(row, ["CENTRO DE CUSTO"]))

        if not cost_center:
            continue

        stores.append({
            "name": normalize_text(get_value(row, ["NOME REFERENCIA"])),
            "geo_name": normalize_text(get_value(row, ["NOME GEO"])),
            "cost_center": cost_center,
            "contracted_headcount": get_value(row, ["QUADROS"]),
            "client": normalize_text(get_value(row, ["CLIENTE"])),
            "state": normalize_text(get_value(row, ["UF"])),
            "zip_code": normalize_text(get_value(row, ["CEP"])),
            "street": normalize_text(get_value(row, ["RUA"])),
            "neighborhood": normalize_text(get_value(row, ["BAIRRO"])),
            "city": normalize_text(get_value(row, ["MUNICIPIO"])),
            "is_active": status in active_statuses,
        })

    return stores
