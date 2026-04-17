from django.urls import path

from .views import divergences_view, dismissals_view, employees_list_view

app_name = "employees"

urlpatterns = [
    path("colaboradores/", employees_list_view, name="employees_list"),
    path("divergencias/", divergences_view, name="divergences"),
    path("demissoes/", dismissals_view, name="dismissals"),
]