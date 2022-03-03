from rest_framework.viewsets import ModelViewSet
from rest_framework import views, response
from . import serializers
from .. import models
from .mixins import SerializerMixin
from ..services import get_statistic
from mainapp.tasks import check_mailing_time


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
    
    def perform_create(self, serializer):
        super().perform_create(serializer)
        check_mailing_time.delay(
            id=serializer.data['id'],
            tag=serializer.data['filter']
        )

    
class StatisticView(views.APIView):
    def get(self, request, *args, **kwargs):
        messages = get_statistic()
        return response.Response(messages)