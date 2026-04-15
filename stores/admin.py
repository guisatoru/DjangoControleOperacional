from django.contrib import admin
from .models import Store


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "cost_center",
        "supervisor",
        "coordinator",
        "client",
        "is_active",
    ]

    search_fields = [
        "name",
        "cost_center",
        "supervisor",
        "coordinator",
        "client",
    ]

    list_filter = [
        "is_active",
        "state",
        "client",
    ]