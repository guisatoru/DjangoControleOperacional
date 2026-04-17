from django.urls import path

from .views import StoreListAPIView

urlpatterns = [
    path("stores/", StoreListAPIView.as_view(), name="api_stores_list"),
]