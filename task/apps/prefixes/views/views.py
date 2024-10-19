from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from task.apps.prefixes.models import Prefix
from task.apps.prefixes.views.serializers import PrefixSerializer


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
