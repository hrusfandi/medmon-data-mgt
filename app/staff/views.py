from rest_framework import viewsets, mixins

from core.models import Staff

from staff import serializers


class StaffViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin):
    """Viewset for staff objects"""
    queryset = Staff.objects.all()
    serializer_class = serializers.StaffSerializer
