from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase


class ImportRunAPITest(TestCase):
    def test_import_requires_file(self):
        response = self.client.post("/api/imports/run/", {})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Selecione pelo menos um arquivo para importar.")

    @patch("imports.api.views.import_stores_from_mother_table")
    @patch("imports.api.views.parse_mother_table_file")
    def test_legacy_single_file_import_still_works(self, mock_parse, mock_import):
        mock_parse.return_value = [{"name": "Loja A"}]
        mock_import.return_value = {"created": 1, "updated": 0}

        uploaded_file = SimpleUploadedFile("mother.xlsx", b"fake-content")

        response = self.client.post(
            "/api/imports/run/",
            {"import_type": "mother_table", "file": uploaded_file},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Importacoes executadas com sucesso.")
        self.assertEqual(response.json()["results"]["mother_table"]["result"]["created"], 1)

    @patch("imports.api.views.import_employees_from_totvs")
    @patch("imports.api.views.parse_totvs_file")
    @patch("imports.api.views.import_stores_from_mother_table")
    @patch("imports.api.views.parse_mother_table_file")
    def test_multiple_imports_can_run_together(
        self,
        mock_parse_mother,
        mock_import_mother,
        mock_parse_totvs,
        mock_import_totvs,
    ):
        mock_parse_mother.return_value = [{"name": "Loja A"}]
        mock_import_mother.return_value = {"created": 1}
        mock_parse_totvs.return_value = [{"employee_code": "1"}]
        mock_import_totvs.return_value = {"created": 2}

        mother_file = SimpleUploadedFile("mother.xlsx", b"fake-content")
        totvs_file = SimpleUploadedFile("totvs.csv", b"fake-content")

        response = self.client.post(
            "/api/imports/run/",
            {
                "mother_table_file": mother_file,
                "totvs_file": totvs_file,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["imported_types"], ["mother_table", "totvs"])
