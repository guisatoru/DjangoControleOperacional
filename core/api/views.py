from rest_framework.response import Response
from rest_framework.views import APIView

from employees.services.query_service import build_employee_summary, get_base_employees_queryset
from stores.services.query_service import build_store_summary, get_base_stores_queryset


class DashboardSummaryAPIView(APIView):
    def get(self, request):
        employees_summary = build_employee_summary(get_base_employees_queryset())
        stores_summary = build_store_summary(list(get_base_stores_queryset()))

        return Response({
            **employees_summary,
            **stores_summary,
        })
