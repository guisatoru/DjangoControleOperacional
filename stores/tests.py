from django.test import TestCase

from employees.models import Employee
from stores.models import Store


class StoreAPITest(TestCase):
    def setUp(self):
        self.store = Store.objects.create(
            name="Loja Centro",
            cost_center="1001",
            contracted_headcount=3,
            management_headcount=2,
            headcount_difference=-1,
            headcount_status="deficit",
            supervisor="Maria",
        )

        Employee.objects.create(
            employee_code="123",
            name="Alice Silva",
            management_store_name="Loja Centro",
            management_status="ATIVO",
            management_job_title="Auxiliar",
            is_active=True,
        )

    def test_store_list_returns_summary(self):
        response = self.client.get("/api/stores/?page=1&filter=all&search=")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["total_items"], 1)
        self.assertEqual(payload["summary"]["total_stores"], 1)

    def test_store_detail_returns_counted_employees(self):
        response = self.client.get(f"/api/stores/{self.store.id}/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["name"], "Loja Centro")
        self.assertEqual(len(payload["counted_employees"]), 1)
