from django.urls import path

from .views import GeoVictoriaSyncAPIView, ImportRunAPIView


urlpatterns = [
    path("imports/run/", ImportRunAPIView.as_view(), name="api_imports_run"),
    path("imports/geovictoria/sync/", GeoVictoriaSyncAPIView.as_view(), name="api_imports_geovictoria_sync"),
]
