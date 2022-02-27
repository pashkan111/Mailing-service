from rest_framework import serializers
from . import models


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Client
        fields = (
            'phone',
            'code',
            'tag',
            'timezone'
            )
        
        
class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Mailing
        fields = (
            'id',
            'date_start',
            'date_finish',
            'text',
            'filter'
        )
        read_only_fields = ('id',)
    