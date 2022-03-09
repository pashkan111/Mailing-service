from rest_framework.test import APIClient
from django.test import TestCase
from mainapp import models
from rest_framework import status
from mainapp.api import serializers
import json


class TestCase1(TestCase):
    
    def setUp(self) -> None:
        self.client = APIClient()
        
    @classmethod
    def setUpTestData(cls):
        client1 = models.Client.objects.create(
            phone="9565453670",
            code="+7",
            tag="clients1",
            timezone="Moscow"
        )
        client2 = models.Client.objects.create(
            phone="9565454440",
            code="+7",
            tag="clients1",
            timezone="Moscow"
        )
        client3 = models.Client.objects.create(
            phone="9565444670",
            code="+8",
            tag="clients2",
            timezone="Asia"
        )
        
    def test_post_client(self):
        body = {
            "phone": "888888",
            "code": "+7",
            "tag": "clients2",
            "timezone": "Moscow"
        }
        response = self.client.post(
            '/api/clients', body, format='json'
        )
        clients_count = models.Client.objects.count()
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(clients_count, 4)
        
    def test_update_client(self):
        client_pk = models.Client.objects.first().pk
        body = {
            "phone": "9999999",
            "tag": "updated",
        }
        response = self.client.patch(
            f'/api/clients/{client_pk}', body, format='json'
        )
        client_updated = models.Client.objects.get(pk=client_pk)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(), serializers.ClientSerializer(client_updated).data
            )
        
    def test_delete_client(self):
        client_pk = models.Client.objects.first().pk
        response = self.client.delete(
            f'/api/clients/{client_pk}', format='json'
        )
        clients_count = models.Client.objects.count()
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(clients_count, 2)
        