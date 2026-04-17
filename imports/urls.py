from django.urls import path

from .views import imports_view

app_name = "imports"

urlpatterns = [
    path("importacoes/", imports_view, name="imports"),
]