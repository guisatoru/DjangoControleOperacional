from rest_framework.response import Response
from rest_framework.views import APIView

from stores.models import Store
from stores.services.query_service import paginate_stores
from .serializers import StoreSerializer, StoreDetailSerializer


class StoreListAPIView(APIView):
    def get(self, request):
        selected_filter = request.GET.get("filter", "all")
        search = request.GET.get("search", "")
        page_number = request.GET.get("page", 1)

        data = paginate_stores(
            selected_filter=selected_filter,
            search=search,
            page_number=page_number,
        )

        serializer = StoreSerializer(data["results"], many=True)

        return Response({
            "page": data["page_obj"].number,
            "total_pages": data["page_obj"].paginator.num_pages,
            "total_items": data["page_obj"].paginator.count,
            "results": serializer.data,
            "summary": data["summary"],
        })


class StoreDetailAPIView(APIView):
    def get(self, request, store_id):
        try:
            store = Store.objects.get(id=store_id)
        except Store.DoesNotExist:
            return Response({"error": "Loja nao encontrada."}, status=404)

        serializer = StoreDetailSerializer(store)
        return Response(serializer.data)
