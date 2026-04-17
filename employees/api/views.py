from rest_framework.response import Response
from rest_framework.views import APIView

from employees.models import Employee
from .serializers import EmployeeSerializer


class EmployeeListAPIView(APIView):
    def get(self, request):
        employees = Employee.objects.filter(
            is_active=True
        ).select_related(
            "store"
        ).order_by(
            "name"
        )

        serializer = EmployeeSerializer(employees, many=True)

        return Response({
            "total_items": employees.count(),
            "results": serializer.data
        })


class EmployeeSummaryAPIView(APIView):
    def get(self, request):
        active_employees = Employee.objects.filter(
            is_active=True
        ).select_related(
            "store"
        )

        active_employees_list = list(active_employees)

        total_employees = len(active_employees_list)

        total_store_divergences = len([
            employee for employee in active_employees_list
            if employee.has_store_divergence()
        ])

        total_status_divergences = len([
            employee for employee in active_employees_list
            if employee.has_status_divergence()
        ])

        total_management_duplicates = len([
            employee for employee in active_employees_list
            if employee.has_management_duplicate_records()
        ])

        total_only_totvs = len([
            employee for employee in active_employees_list
            if not employee.management_status
        ])

        return Response({
            "total_employees": total_employees,
            "total_store_divergences": total_store_divergences,
            "total_status_divergences": total_status_divergences,
            "total_management_duplicates": total_management_duplicates,
            "total_only_totvs": total_only_totvs,
        })


class EmployeeDetailAPIView(APIView):
    def get(self, request, employee_id):
        try:
            employee = Employee.objects.select_related("store").get(
                id=employee_id
            )
        except Employee.DoesNotExist:
            return Response(
                {
                    "error": "Colaborador não encontrado."
                },
                status=404
            )

        serializer = EmployeeSerializer(employee)

        return Response(serializer.data)