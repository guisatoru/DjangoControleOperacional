from rest_framework.response import Response
from rest_framework.views import APIView

from stores.models import Store
from .serializers import StoreSerializer

class StoreListAPIView(APIView):
    def get(self, request):
        stores = Store.objects.filter(
            contracted_headcount__isnull=False,
            contracted_headcount__gt=0,
        ).order_by("name")

        serializer = StoreSerializer(stores, many=True)

        return Response({
            "total_items": stores.count(),
            "results": serializer.data
        })