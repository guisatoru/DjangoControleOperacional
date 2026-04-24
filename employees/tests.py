from django.test import TestCase

from employees.models import Employee
from stores.models import Store


class EmployeeAPITest(TestCase):
    def setUp(self):
        self.store = Store.objects.create(
            name="Loja Centro",
            cost_center="1001",
            contracted_headcount=2,
        )

        self.employee = Employee.objects.create(
            employee_code="123",
            name="Alice Silva",
            store=self.store,
            management_store_name="Loja Centro",
            management_status="ATIVO",
            payroll_status="A",
            is_active=True,
        )

        Employee.objects.create(
            employee_code="456",
            name="Bruno Souza",
            store=self.store,
            management_status="",
            is_active=True,
        )

    def test_employee_list_is_paginated(self):
        response = self.client.get("/api/employees/?page=1&filter=all&search=")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["total_items"], 2)
        self.assertEqual(len(payload["results"]), 2)

    def test_employee_summary_returns_totals(self):
        response = self.client.get("/api/employees/summary/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["total_employees"], 2)

    def test_employee_detail_returns_requested_record(self):
        response = self.client.get(f"/api/employees/{self.employee.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["employee_code"], "123")
