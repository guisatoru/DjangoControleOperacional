from django.urls import path

from .views import EmployeeListAPIView, EmployeeSummaryAPIView, EmployeeDetailAPIView

urlpatterns = [
    path("employees/", EmployeeListAPIView.as_view(), name="api_employees_list"),
    path("employees/summary/", EmployeeSummaryAPIView.as_view(), name="api_employees_summary"),
    path("employees/<int:employee_id>/", EmployeeDetailAPIView.as_view(), name="api_employees_detail"),
]
