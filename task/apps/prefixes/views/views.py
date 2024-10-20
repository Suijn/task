import structlog
from django.db import IntegrityError
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from task.apps.prefixes.models import Prefix
from task.apps.prefixes.views.serializers import PrefixSerializer

logger = structlog.get_logger()


class PrefixViewSet(viewsets.ViewSet):
    @extend_schema(
        responses={200: PrefixSerializer},
    )
    def list(self, request):
        queryset = Prefix.objects.all().prefetch_related("items")
        serializer = PrefixSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk: int | None = None):
        queryset = Prefix.objects.all().prefetch_related("items")
        prefix = get_object_or_404(queryset, pk=pk)
        serializer = PrefixSerializer(prefix)
        return Response(serializer.data)

    def create(self, request):
        data_in = request.data
        log = logger.bind(data_in=data_in)

        serializer = PrefixSerializer(data=data_in)
        serializer.is_valid(raise_exception=True)
        clean_data = serializer.validated_data

        try:
            prefix = Prefix.objects.create(name=clean_data["name"])
            log.info("Created a new Prefix.", name=clean_data["name"])
        except IntegrityError:
            log.error("Creating Prefix failed.", reason="Prefix already exists.")
            msg = {"conflict": "Prefix already exists."}
            return Response(msg, status=409)
        else:
            serializer = PrefixSerializer(
                prefix,
                context={
                    "overwrite_schema_out": True,
                    "serialize_attributes": ("name",),
                },
            )
            return Response(serializer.data, status=201)
