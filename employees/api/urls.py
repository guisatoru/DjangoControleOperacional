from django.urls import path

from .views import (
    DismissalDetailAPIView,
    DismissalListAPIView,
    EmployeeDetailAPIView,
    EmployeeListAPIView,
    EmployeeSummaryAPIView,
    TerminationControlCreateAPIView,
    TerminationDetailAPIView,
    TerminationListAPIView,
    TerminationTimeOffSummaryAPIView,
)

urlpatterns = [
    path("employees/", EmployeeListAPIView.as_view(), name="api_employees_list"),
    path("employees/summary/", EmployeeSummaryAPIView.as_view(), name="api_employees_summary"),
    path("employees/<int:employee_id>/", EmployeeDetailAPIView.as_view(), name="api_employees_detail"),
    path("dismissals/", DismissalListAPIView.as_view(), name="api_dismissals_list"),
    path("dismissals/<int:dismissal_id>/", DismissalDetailAPIView.as_view(), name="api_dismissals_detail"),
    path("terminations/", TerminationListAPIView.as_view(), name="api_terminations_list"),
    path("terminations/<int:termination_id>/", TerminationDetailAPIView.as_view(), name="api_terminations_detail"),
    path("terminations/<int:termination_id>/timeoff/", TerminationTimeOffSummaryAPIView.as_view(), name="api_terminations_timeoff"),
    path("terminations/<int:termination_id>/control/", TerminationControlCreateAPIView.as_view(), name="api_terminations_control_create"),
]
