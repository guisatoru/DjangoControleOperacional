from rest_framework.response import Response
from rest_framework.views import APIView

from core.utils.normalizers import normalize_column_name
from employees.models import Employee
from stores.models import Store
from .serializers import StoreSerializer

MANAGEMENT_STATUSES_THAT_COUNT = [
    "ATIVO",
    "AVISO",
    "FERIAS",
]

def management_status_counts_in_headcount(status):
    normalized_status = normalize_column_name(status)

    return normalized_status in MANAGEMENT_STATUSES_THAT_COUNT


def names_match(first_name, second_name):
    normalized_first_name = normalize_column_name(first_name)
    normalized_second_name = normalize_column_name(second_name)

    return normalized_first_name == normalized_second_name


def get_management_employees_for_store(store, employees):
    store_name = store.name

    matched_employees = []

    for employee in employees:
        if not employee.management_store_name:
            continue

        if not names_match(employee.management_store_name, store_name):
            continue

        if not management_status_counts_in_headcount(employee.management_status):
            continue

        matched_employees.append(employee)

    return matched_employees


class StoreListAPIView(APIView):
    def get(self, request):
        stores = Store.objects.filter(
            contracted_headcount__isnull=False,
            contracted_headcount__gt=0,
        ).order_by("name")

        employees = Employee.objects.all()

        valid_stores = []

        for store in stores:
            management_employees = get_management_employees_for_store(
                store,
                employees,
            )

            if len(management_employees) == 0:
                continue

            store.management_headcount = len(management_employees)
            store.headcount_difference = (
                store.management_headcount - store.contracted_headcount
            )

            if store.headcount_difference > 0:
                store.headcount_status = "excess"
            elif store.headcount_difference < 0:
                store.headcount_status = "deficit"
            else:
                store.headcount_status = "balanced"

            valid_stores.append(store)

        serializer = StoreSerializer(valid_stores, many=True)

        return Response({
            "total_items": len(valid_stores),
            "results": serializer.data
        })
