from rest_framework import serializers

from employees.api.serializers import EmployeeSerializer
from stores.models import Store
from stores.services.query_service import get_store_counted_employees


class StoreSerializer(serializers.ModelSerializer):
    management_store_name = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = [
            "id",
            "name",
            "management_store_name",
            "geo_name",
            "cost_center",
            "contracted_headcount",
            "management_headcount",
            "headcount_difference",
            "headcount_status",
            "supervisor",
            "coordinator",
            "street",
            "neighborhood",
            "city",
            "state",
            "zip_code",
            "client",
            "is_active",
        ]

    def get_management_store_name(self, store):
        return store.name


class StoreDetailSerializer(StoreSerializer):
    counted_employees = serializers.SerializerMethodField()

    class Meta(StoreSerializer.Meta):
        fields = StoreSerializer.Meta.fields + [
            "counted_employees",
        ]

    def get_counted_employees(self, store):
        employees = get_store_counted_employees(store)
        return EmployeeSerializer(employees, many=True).data
