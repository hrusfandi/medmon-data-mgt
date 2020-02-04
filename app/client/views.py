from rest_framework import viewsets, mixins

from core.models import Client

from client import serializers


class ClientViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    """Viewset for client objects"""
    queryset = Client.objects.all().order_by('-name')
    serializer_class = serializers.ClientSerializer
