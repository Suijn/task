from rest_framework import serializers

from task.apps.prefixes.models import Prefix


class PrefixSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    items = serializers.StringRelatedField(many=True, read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Prefix
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Sometimes we need to overwrite the response schema.
        if self.context.get("overwrite_schema_out"):
            # Serialize only the specified attributes.
            representation = {}
            attributes_to_serialize = self.context["serialize_attributes"]
            for attr in attributes_to_serialize:
                representation[attr] = getattr(instance, attr)
        return representation
