from rest_framework.viewsets import ModelViewSet
from rest_framework import views, response
from . import serializers
from .. import models
from .mixins import SerializerMixin
from ..services import get_statistic
from service.settings import env

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
    
    
class StatisticView(views.APIView):
    def get(self, request, *args, **kwargs):

        print(env('SERVICE_URL'))
        messages = get_statistic()
        return response.Response(messages)