from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("employees.urls")),
    path("", include("imports.urls")),

    path("api/", include("employees.api.urls")),
    path("api/", include("stores.api.urls")),
]
