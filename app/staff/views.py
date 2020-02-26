from rest_framework import viewsets, mixins

from core.authentication import JWTAuthentication
from core.models import Staff

from staff import serializers


class StaffViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin):
    """Viewset for staff objects"""
    authentication_classes = (JWTAuthentication,)

    queryset = Staff.objects.all()
    serializer_class = serializers.StaffSerializer
