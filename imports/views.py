import os
import tempfile

from django.shortcuts import render
from django.contrib import messages

from imports.parsers.mother_table_parser import parse_mother_table_file
from imports.parsers.totvs_parser import parse_totvs_file
from imports.parsers.management_parser import (
    parse_management_employees_file,
    parse_management_supervision_file,
)

from imports.services.store_importer import import_stores_from_mother_table
from imports.services.employee_importer import import_employees_from_totvs
from imports.services.management_employee_importer import import_management_employees
from imports.services.management_supervision_importer import import_management_supervision


def save_uploaded_file_temporarily(uploaded_file):
    suffix = os.path.splitext(uploaded_file.name)[1]

    temporary_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)

    for chunk in uploaded_file.chunks():
        temporary_file.write(chunk)

    temporary_file.close()

    return temporary_file.name


def imports_view(request):
    result = None

    if request.method == "POST":
        import_type = request.POST.get("import_type")
        uploaded_file = request.FILES.get("file")

        if not uploaded_file:
            messages.error(request, "Selecione um arquivo para importar.")
            return render(request, "imports/imports.html", {"result": result})

        temporary_file_path = save_uploaded_file_temporarily(uploaded_file)

        try:
            if import_type == "mother_table":
                parsed_stores = parse_mother_table_file(temporary_file_path)
                result = import_stores_from_mother_table(parsed_stores)
                messages.success(request, "Tabela Mãe importada com sucesso.")

            elif import_type == "totvs":
                parsed_employees = parse_totvs_file(temporary_file_path)
                result = import_employees_from_totvs(parsed_employees)
                messages.success(request, "TOTVS importado com sucesso.")

            elif import_type == "management":
                parsed_employees = parse_management_employees_file(temporary_file_path)
                employee_result = import_management_employees(parsed_employees)

                parsed_stores = parse_management_supervision_file(temporary_file_path)
                supervision_result = import_management_supervision(parsed_stores)

                result = {
                    "employees": employee_result,
                    "supervision": supervision_result,
                }

                messages.success(request, "Gestão de Pessoas importada com sucesso.")

            else:
                messages.error(request, "Tipo de importação inválido.")

        except Exception as error:
            messages.error(request, f"Erro ao importar arquivo: {error}")

        finally:
            if os.path.exists(temporary_file_path):
                os.remove(temporary_file_path)

    return render(request, "imports/imports.html", {"result": result})