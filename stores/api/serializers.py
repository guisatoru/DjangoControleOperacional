from rest_framework import serializers

from stores.models import Store

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = [
            "id",
            "name",
            "management_link_name",
            "geo_name",
            "cost_center",
            "contracted_headcount",
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
