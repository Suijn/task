from rest_framework import serializers

from task.apps.prefixes.models import Item, Prefix


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


class ItemSerializerOut(serializers.ModelSerializer):
    """Handle serialization of Items."""

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    prefix = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Item
        fields = ["id", "name", "prefix"]


class ItemSerializerIn(serializers.ModelSerializer):
    """Handle deserialization of items."""

    prefix = serializers.IntegerField(write_only=True)

    class Meta:
        model = Item
        fields = ["prefix"]


class ConflictSerializerOut(serializers.Serializer):
    """Serialize conflicts."""

    conflict = serializers.CharField(read_only=True)
