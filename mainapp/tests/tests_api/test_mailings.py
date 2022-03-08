import datetime
from rest_framework.test import APIClient
from django.test import TestCase
from mainapp import models
from rest_framework import status
from mainapp.api import serializers


class TestCase1(TestCase):
    
    def setUp(self) -> None:
        self.client = APIClient()
        
    @classmethod
    def setUpTestData(cls):
        mailing1 = models.Mailing.objects.create(
            date_start = datetime.datetime.strptime('2022-03-06 13:10:23', '%Y-%m-%d %H:%M:%S'),
            date_finish = datetime.datetime.strptime('2022-03-08 13:10:23', '%Y-%m-%d %H:%M:%S'),
            text = 'hello',
            filter = 'clients_1'
        )
        mailing2 = models.Mailing.objects.create(
            date_start = datetime.datetime.strptime('2022-03-03 13:10:23', '%Y-%m-%d %H:%M:%S'),
            date_finish = datetime.datetime.strptime('2022-03-04 13:10:23', '%Y-%m-%d %H:%M:%S'),
            text = 'goodbye',
            filter = 'clients_1'
        )
        mailing3 = models.Mailing.objects.create(
            date_start = datetime.datetime.strptime('2022-03-08 13:10:23', '%Y-%m-%d %H:%M:%S'),
            date_finish = datetime.datetime.strptime('2022-03-08 14:10:23', '%Y-%m-%d %H:%M:%S'),
            text = 'how are you?',
            filter = 'clients_1',
            is_sent = True
        )
    
    def test_get_all_mailings(self):
        response = self.client.get('/api/mailings')
        mailings = models.Mailing.objects.all()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(), serializers.MailingSerializer(mailings, many=True).data
        )
        
    def test_create_mailing(self):
        body = {
            "date_start": "2022-03-08T23:16:34.871Z",
            "date_finish": "2022-03-08T23:16:34.871Z",
            "text": "post-test",
            "filter": "clients2"
        }
        response = self.client.post(
            '/api/mailings', body, format='json'
            )
        mailings_count = models.Mailing.objects.count()
    
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(mailings_count, 4)
        