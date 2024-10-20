import structlog
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from task.apps.prefixes.models import Item, Prefix
from task.apps.prefixes.views.serializers import (
    ConflictSerializerOut,
    ItemSerializerIn,
    ItemSerializerOut,
    PrefixSerializer,
)

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


class ItemViewSet(viewsets.ViewSet):
    @extend_schema(
        request=ItemSerializerIn,
        responses={200: ItemSerializerOut, 409: ConflictSerializerOut},
    )
    def partial_update(self, request, pk: int):
        data_in = request.data
        log = logger.bind(item_pk=pk, data_in=data_in)

        serializer_in = ItemSerializerIn(data=data_in)
        serializer_in.is_valid(raise_exception=True)

        try:
            item = Item.objects.get(pk=pk)
        except ObjectDoesNotExist:
            log.error("Updating Item failed.", reason=settings.CONFLICT_ITEM_NOT_FOUND)
            conflict = {"conflict": settings.CONFLICT_ITEM_NOT_FOUND}
            return Response(ConflictSerializerOut(conflict).data, status=409)

        try:
            new_prefix = Prefix.objects.get(pk=serializer_in.validated_data["prefix"])
        except ObjectDoesNotExist:
            log.error(
                "Updating Item failed.", reason=settings.CONFLICT_PREFIX_NOT_FOUND
            )
            conflict = {"conflict": settings.CONFLICT_PREFIX_NOT_FOUND}
            return Response(ConflictSerializerOut(conflict).data, status=409)

        item.prefix = new_prefix
        item.save()
        log.info("Updated Item", with_data=data_in)

        serializer_out = ItemSerializerOut(item)
        return Response(serializer_out.data)

    @extend_schema(
        responses={200: ItemSerializerOut},
    )
    def list(self, request):
        queryset = Item.objects.all()
        serializer = ItemSerializerOut(queryset, many=True)
        return Response(serializer.data)
