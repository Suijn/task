from rest_framework import serializers

from task.apps.prefixes.models import Item, Prefix


class PrefixSerializerIn(serializers.ModelSerializer):
    """Handle deserialization."""

    name = serializers.CharField(write_only=True)

    class Meta:
        model = Prefix
        fields = ["name"]


class PrefixSerializerOut(serializers.ModelSerializer):
    """Handle serialization."""

    name = serializers.CharField(read_only=True)
    items = serializers.StringRelatedField(read_only=True, many=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Prefix
        fields = ["id", "name", "items"]


class PrefixSerializerOutOnlyName(serializers.ModelSerializer):
    """Handle deserialization."""

    name = serializers.CharField(read_only=True)

    class Meta:
        model = Prefix
        fields = ["name"]


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
