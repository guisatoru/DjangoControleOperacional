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


def parse_mother_table_file(file_path):
    dataframe = pd.read_excel(
        file_path,
        sheet_name="MÃE COM PROCS",
        dtype=str,
    )

    dataframe = normalize_dataframe_columns(dataframe)

    stores = []

    active_statuses = ["ATIVO", "FORA DA GESTAO", "FORA DA GESTÃO"]

    for _, row in dataframe.iterrows():
        status = normalize_text(get_value(row, ["STATUS"])).upper()

        cost_center = normalize_cost_center(
            get_value(row, ["CENTRO DE CUSTO"])
        )

        if not cost_center:
            continue

        store_data = {
            "name": normalize_text(
                get_value(row, ["NOME REFERENCIA"])
            ),
            "geo_name": normalize_text(
                get_value(row, ["NOME GEO"])
            ),
            "cost_center": cost_center,
            "contracted_headcount": get_value(row, ["QUADROS"]),
            "client": normalize_text(
                get_value(row, ["CLIENTE"])
            ),
            "state": normalize_text(
                get_value(row, ["UF"])
            ),
            "zip_code": normalize_text(
                get_value(row, ["CEP"])
            ),
            "street": normalize_text(
                get_value(row, ["RUA"])
            ),
            "neighborhood": normalize_text(
                get_value(row, ["BAIRRO"])
            ),
            "is_active": status in active_statuses,
        }

        stores.append(store_data)

    return stores