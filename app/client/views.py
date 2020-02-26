from rest_framework import viewsets, mixins

from core.authentication import JWTAuthentication
from core.models import Client

from client import serializers


class ClientViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    """Viewset for client objects"""
    authentication_classes = (JWTAuthentication,)

    queryset = Client.objects.all().order_by('-name')
    serializer_class = serializers.ClientSerializer
