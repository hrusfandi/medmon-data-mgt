from rest_framework import serializers

from core.models import Client


class ClientSerializer(serializers.ModelSerializer):
    """Serializer for client objects"""

    class Meta:
        model = Client
        fields = ('id', 'name', 'address', 'contact',)
        read_only_fields = ('id',)
