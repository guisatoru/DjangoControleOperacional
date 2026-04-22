from rest_framework import serializers

from stores.models import Store


class StoreSerializer(serializers.ModelSerializer):
    management_store_name = serializers.SerializerMethodField()
    management_headcount = serializers.SerializerMethodField()
    headcount_difference = serializers.SerializerMethodField()
    headcount_status = serializers.SerializerMethodField()

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

    def get_management_headcount(self, store):
        return getattr(store, "management_headcount", 0)

    def get_headcount_difference(self, store):
        return getattr(store, "headcount_difference", 0)

    def get_headcount_status(self, store):
        return getattr(store, "headcount_status", "balanced")