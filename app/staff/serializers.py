from rest_framework import serializers

from core.models import Staff


class StaffSerializer(serializers.ModelSerializer):
    """Serializer for staff objects"""

    class Meta:
        model = Staff
        fields = ('id', 'name', 'address', 'contact', 'NIP',)
        read_only_fields = ('id',)
