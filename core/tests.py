from django.test import TestCase

from employees.models import Employee
from stores.models import Store


class DashboardSummaryAPITest(TestCase):
    def setUp(self):
        self.store = Store.objects.create(
            name="Loja Centro",
            cost_center="1001",
            contracted_headcount=3,
            management_headcount=2,
            headcount_difference=-1,
            headcount_status="deficit",
        )

        Employee.objects.create(
            employee_code="1",
            name="Alice",
            store=self.store,
            management_store_name="Loja Centro",
            management_status="ATIVO",
            is_active=True,
        )

    def test_dashboard_summary_returns_aggregated_data(self):
        response = self.client.get("/api/dashboard/summary/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["total_employees"], 1)
        self.assertEqual(response.json()["total_stores"], 1)
        self.assertEqual(response.json()["total_deficit"], 1)
