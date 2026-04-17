from django.db.models import Count, Q

from rest_framework.response import Response
from rest_framework.views import APIView

from stores.models import Store
from .serializers import StoreSerializer


class StoreListAPIView(APIView):
    def get(self, request):
        stores = Store.objects.annotate(
            active_headcount_employees=Count(
                "employees",
                filter=Q(
                    employees__is_active=True,
                    employees__counts_in_store_headcount=True,
                ),
            )
        ).filter(
            contracted_headcount__isnull=False,
            contracted_headcount__gt=0,
            active_headcount_employees__gt=0,
        ).order_by("name")

        serializer = StoreSerializer(stores, many=True)

        return Response({
            "total_items": stores.count(),
            "results": serializer.data
        })