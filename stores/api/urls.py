from django.urls import path

from .views import StoreDetailAPIView, StoreListAPIView

urlpatterns = [
    path("stores/", StoreListAPIView.as_view(), name="api_stores_list"),
    path("stores/<int:store_id>/", StoreDetailAPIView.as_view(), name="api_stores_detail"),
]
