from rest_framework.viewsets import ModelViewSet
from . import serializers
from . import models
from .mixins import SerializerMixin


class ClientViewSet(ModelViewSet):
    serializer_class = serializers.ClientSerializer
    queryset = models.Client.objects.all()
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, partial=True, **kwargs)
    
    
class MailingViewSet(SerializerMixin, ModelViewSet):
    serializer_class = serializers.MailingSerializer
    queryset = models.Mailing.objects.all()
    serializer_classes_by_action = {
        "retrieve": serializers.MailingStisticSerializer
        }
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, partial=True, **kwargs)
    