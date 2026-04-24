from django.urls import path

from .views import DashboardSummaryAPIView


urlpatterns = [
    path("dashboard/summary/", DashboardSummaryAPIView.as_view(), name="api_dashboard_summary"),
]
