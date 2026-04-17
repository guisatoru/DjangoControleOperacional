from django.urls import path

from .views import divergences_view, dismissals_view

app_name = "employees"

urlpatterns = [
    path("divergencias/", divergences_view, name="divergences"),
    path("demissoes/", dismissals_view, name="dismissals"),
]