from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("core.api.urls")),
    path("api/", include("employees.api.urls")),
    path("api/", include("imports.api.urls")),
    path("api/", include("stores.api.urls")),
]
