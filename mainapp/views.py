from rest_framework.viewsets import ModelViewSet
from . import serializers
from . import models


class ClientViewSet(ModelViewSet):
    serializer_class = serializers.ClientSerializer
    queryset = models.Client.objects.all()