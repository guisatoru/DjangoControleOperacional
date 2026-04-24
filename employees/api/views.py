from rest_framework.response import Response
from rest_framework.views import APIView

from employees.models import Employee
from employees.services.query_service import get_employee_summary, paginate_employees
from .serializers import EmployeeSerializer


class EmployeeListAPIView(APIView):
    def get(self, request):
        selected_filter = request.GET.get("filter", "all")
        search = request.GET.get("search", "")
        page_number = request.GET.get("page", 1)

        data = paginate_employees(
            selected_filter=selected_filter,
            search=search,
            page_number=page_number,
        )

        serializer = EmployeeSerializer(data["results"], many=True)

        return Response({
            "page": data["page_obj"].number,
            "total_pages": data["page_obj"].paginator.num_pages,
            "total_items": data["page_obj"].paginator.count,
            "results": serializer.data,
        })


class EmployeeSummaryAPIView(APIView):
    def get(self, request):
        return Response(get_employee_summary())


class EmployeeDetailAPIView(APIView):
    def get(self, request, employee_id):
        try:
            employee = Employee.objects.select_related("store").get(id=employee_id)
        except Employee.DoesNotExist:
            return Response({"error": "Colaborador nao encontrado."}, status=404)

        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)
