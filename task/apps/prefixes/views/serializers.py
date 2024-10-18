from rest_framework import serializers

from task.apps.prefixes.models import Prefix


class PrefixSerializer(serializers.ModelSerializer):
    items = serializers.StringRelatedField(many=True)

    class Meta:
        model = Prefix
        fields = ["name", "items", "pk"]
