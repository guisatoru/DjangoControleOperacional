import os
import tempfile

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from imports.parsers.management_parser import (
    parse_management_employees_file,
    parse_management_supervision_file,
)
from imports.parsers.mother_table_parser import parse_mother_table_file
from imports.parsers.totvs_parser import parse_totvs_file
from imports.services.employee_importer import import_employees_from_totvs
from imports.services.geovictoria_sync import sync_geovictoria_data
from imports.services.management_employee_importer import import_management_employees
from imports.services.management_supervision_importer import import_management_supervision
from imports.services.store_importer import import_stores_from_mother_table


IMPORT_TYPE_TO_FILE_FIELD = {
    "mother_table": "mother_table_file",
    "totvs": "totvs_file",
    "management": "management_file",
}


def save_uploaded_file_temporarily(uploaded_file):
    suffix = os.path.splitext(uploaded_file.name)[1]
    temporary_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)

    for chunk in uploaded_file.chunks():
        temporary_file.write(chunk)

    temporary_file.close()
    return temporary_file.name


def process_mother_table_import(temporary_file_path):
    parsed_stores = parse_mother_table_file(temporary_file_path)
    return {
        "message": "Tabela Mae importada com sucesso.",
        "result": import_stores_from_mother_table(parsed_stores),
    }


def process_totvs_import(temporary_file_path):
    parsed_employees = parse_totvs_file(temporary_file_path)
    return {
        "message": "TOTVS importado com sucesso.",
        "result": import_employees_from_totvs(parsed_employees),
    }


def process_management_import(temporary_file_path):
    parsed_employees = parse_management_employees_file(temporary_file_path)
    employee_result = import_management_employees(parsed_employees)

    parsed_stores = parse_management_supervision_file(temporary_file_path)
    supervision_result = import_management_supervision(parsed_stores)

    return {
        "message": "Gestao de Pessoas importada com sucesso.",
        "result": {
            "employees": employee_result,
            "supervision": supervision_result,
        },
    }


IMPORT_PROCESSORS = {
    "mother_table": process_mother_table_import,
    "totvs": process_totvs_import,
    "management": process_management_import,
}


def collect_import_files(request):
    import_files = {
        import_key: request.FILES.get(file_field_name)
        for import_key, file_field_name in IMPORT_TYPE_TO_FILE_FIELD.items()
    }

    legacy_import_type = request.data.get("import_type")
    legacy_file = request.FILES.get("file")

    if legacy_import_type and legacy_file:
        import_files[legacy_import_type] = legacy_file

    return {
        import_key: uploaded_file
        for import_key, uploaded_file in import_files.items()
        if uploaded_file
    }


def run_single_import(import_key, uploaded_file):
    if import_key not in IMPORT_PROCESSORS:
        raise ValueError("Tipo de importacao invalido.")

    temporary_file_path = save_uploaded_file_temporarily(uploaded_file)

    try:
        return IMPORT_PROCESSORS[import_key](temporary_file_path)
    finally:
        if os.path.exists(temporary_file_path):
            os.remove(temporary_file_path)


class ImportRunAPIView(APIView):
    def post(self, request):
        selected_imports = collect_import_files(request)

        if not selected_imports:
            return Response(
                {"error": "Selecione pelo menos um arquivo para importar."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        results = {}

        try:
            for import_key, uploaded_file in selected_imports.items():
                results[import_key] = run_single_import(import_key, uploaded_file)
        except ValueError as error:
            return Response({"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(
                {"error": f"Erro ao importar arquivo: {error}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({
            "message": "Importacoes executadas com sucesso.",
            "results": results,
            "imported_types": list(results.keys()),
        })


class GeoVictoriaSyncAPIView(APIView):
    def post(self, request):
        try:
            summary = sync_geovictoria_data()
        except ValueError as error:
            return Response({"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(
                {"error": f"Erro ao sincronizar GeoVictoria: {error}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({
            "message": "Sincronizacao com GeoVictoria concluida com sucesso.",
            "result": summary,
        })
