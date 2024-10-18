from rest_framework import viewsets
from rest_framework.response import Response

from task.apps.prefixes.models import Prefix
from task.apps.prefixes.views.serializers import PrefixSerializer


class PrefixViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Prefix.objects.all().prefetch_related("items")
        serializer = PrefixSerializer(queryset, many=True)
        return Response(serializer.data)
