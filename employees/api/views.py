from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from employees.models import DismissalRecord, Employee
from employees.services.dismissal_query_service import paginate_dismissals
from employees.services.query_service import get_employee_summary, paginate_employees
from employees.services.termination_service import (
    create_termination_control,
    get_termination_detail,
    paginate_terminations,
)
from imports.services.geovictoria_sync import get_geovictoria_timeoff_summary
from .dismissal_serializers import DismissalRecordSerializer
from .serializers import EmployeeSerializer


class EmployeeListAPIView(APIView):
    def get(self, request):
        selected_filter = request.GET.get("filter", "all")
        search = request.GET.get("search", "")
        page_number = request.GET.get("page", 1)

        data = paginate_employees(
            selected_filter=selected_filter,
            search=search,
            page_number=page_number,
        )

        serializer = EmployeeSerializer(data["results"], many=True)

        return Response({
            "page": data["page_obj"].number,
            "total_pages": data["page_obj"].paginator.num_pages,
            "total_items": data["page_obj"].paginator.count,
            "results": serializer.data,
        })


class EmployeeSummaryAPIView(APIView):
    def get(self, request):
        return Response(get_employee_summary())


class EmployeeDetailAPIView(APIView):
    def get(self, request, employee_id):
        try:
            employee = Employee.objects.select_related("store").get(id=employee_id)
        except Employee.DoesNotExist:
            return Response({"error": "Colaborador nao encontrado."}, status=404)

        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)


class DismissalListAPIView(APIView):
    def get(self, request):
        selected_filter = request.GET.get("filter", "all")
        search = request.GET.get("search", "")
        page_number = request.GET.get("page", 1)

        data = paginate_dismissals(
            selected_filter=selected_filter,
            search=search,
            page_number=page_number,
        )

        serializer = DismissalRecordSerializer(data["results"], many=True)

        return Response({
            "page": data["page_obj"].number,
            "total_pages": data["page_obj"].paginator.num_pages,
            "total_items": data["page_obj"].paginator.count,
            "results": serializer.data,
            "summary": data["summary"],
        })


class DismissalDetailAPIView(APIView):
    def get(self, request, dismissal_id):
        try:
            dismissal_record = DismissalRecord.objects.get(id=dismissal_id)
        except DismissalRecord.DoesNotExist:
            return Response({"error": "Demissao nao encontrada."}, status=404)

        serializer = DismissalRecordSerializer(dismissal_record)
        return Response(serializer.data)


class TerminationListAPIView(APIView):
    def get(self, request):
        selected_filter = request.GET.get("filter", "all")
        search = request.GET.get("search", "")
        page_number = request.GET.get("page", 1)
        date_from = request.GET.get("date_from", "")
        coordinator = request.GET.get("coordinator", "all")

        data = paginate_terminations(
            selected_filter=selected_filter,
            search=search,
            page_number=page_number,
            date_from=date_from,
            coordinator=coordinator,
        )

        return Response({
            "page": data["page_obj"].number,
            "total_pages": data["page_obj"].paginator.num_pages,
            "total_items": data["page_obj"].paginator.count,
            "results": data["results"],
            "summary": data["summary"],
            "coordinators": data["coordinators"],
        })


class TerminationDetailAPIView(APIView):
    def get(self, request, termination_id):
        termination = get_termination_detail(termination_id)

        if not termination:
            return Response({"error": "Termino nao encontrado."}, status=404)

        return Response(termination)


class TerminationTimeOffSummaryAPIView(APIView):
    def get(self, request, termination_id):
        termination = get_termination_detail(termination_id)

        if not termination:
            return Response({"error": "Termino nao encontrado."}, status=404)

        if not termination.get("geo_user_id"):
            return Response({"error": "Este colaborador ainda nao possui Identifier da GeoVictoria."}, status=400)

        if not termination.get("admission_date"):
            return Response({"error": "Este colaborador nao possui data de admissao para consultar afastamentos."}, status=400)

        try:
            summary = get_geovictoria_timeoff_summary(
                start_date=termination["admission_date"].isoformat(),
                end_date=timezone.localdate().isoformat(),
                user_id=termination["geo_user_id"],
            )
        except ValueError as error:
            return Response({"error": str(error)}, status=400)

        return Response(summary)


class TerminationControlCreateAPIView(APIView):
    def post(self, request, termination_id):
        stage = request.data.get("stage")
        action = request.data.get("action")
        observation = (request.data.get("observation") or "").strip()
        responded_by = (request.data.get("responded_by") or "Usuario").strip()

        if action not in ["prorrogado", "termino", "manter"]:
            return Response({"error": "Acao invalida para o controle de termino."}, status=400)

        if stage not in [1, 2, "1", "2"]:
            return Response({"error": "Etapa invalida para o controle de termino."}, status=400)

        normalized_stage = int(stage)

        if normalized_stage == 1 and action not in ["prorrogado", "termino"]:
            return Response({"error": "No 1o termino so e permitido prorrogar ou dar termino."}, status=400)

        if normalized_stage == 2 and action not in ["manter", "termino"]:
            return Response({"error": "No 2o termino so e permitido manter ou dar termino."}, status=400)

        if not observation:
            return Response({"error": "A observacao e obrigatoria."}, status=400)

        termination = get_termination_detail(termination_id)

        if not termination:
            return Response({"error": "Termino nao encontrado."}, status=404)

        if termination["closed"]:
            return Response({"error": "Este acompanhamento ja foi encerrado."}, status=400)

        try:
            create_termination_control(
                employee_id=termination_id,
                stage=normalized_stage,
                action=action,
                observation=observation,
                responded_by=responded_by,
            )
        except Employee.DoesNotExist:
            return Response({"error": "Colaborador nao encontrado para controle de termino."}, status=404)
        except ValidationError as error:
            return Response({"error": str(error)}, status=400)

        termination = get_termination_detail(termination_id)
        return Response({
            "message": "Controle de termino registrado com sucesso.",
            "termination": termination,
        }, status=201)
