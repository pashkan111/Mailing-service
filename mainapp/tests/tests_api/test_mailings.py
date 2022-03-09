import datetime
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
        
        message1 = models.Message.objects.create(
            status=models.Message.DELIVERED,
            mailing=mailing1
        )
        message2 = models.Message.objects.create(
            status=models.Message.DELIVERED,
            mailing=mailing1
        )
        message3 = models.Message.objects.create(
            status=models.Message.IN_PROGRESS,
            mailing=mailing1
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
        
    def test_update_mailing(self):
        mailing_pk = models.Mailing.objects.first().pk
        body = {
            "text": "updated",
            "filter": "updated"
        }
        response = self.client.patch(
            f'/api/mailings/{mailing_pk}', body, format='json'
        )
        mailing_updated = models.Mailing.objects.get(pk=mailing_pk)
        
        self.assertEqual(
            response.json(), serializers.MailingSerializer(mailing_updated).data
        )
        self.assertEqual(mailing_updated.text, 'updated')
        
    def test_delete_mailing(self):
        mailing_pk = models.Mailing.objects.first().pk
        response = self.client.delete(
            f'/api/mailings/{mailing_pk}', format='json'
        )
        mailings_count = models.Mailing.objects.count()
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(mailings_count, 2)
        
    def test_get_statistics(self):
        response = self.client.get('/api/message-statistic')
        mailing_pk = models.Mailing.objects.first().pk
        response_data = response.json()
        statistic_data_delivered = response_data.get(str(mailing_pk))[0]
        statistic_data_progress = response_data.get(str(mailing_pk))[1]
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(statistic_data_delivered['status'], 'delivered')
        self.assertEqual(statistic_data_delivered['total'], 2)
        self.assertEqual(statistic_data_progress['status'], 'progress')
        self.assertEqual(statistic_data_progress['total'], 1)
        
    def test_retrieve_mailing(self):
        mailing_pk = models.Mailing.objects.first().pk
        response = self.client.get(f'/api/mailings/{mailing_pk}')
        messages_list = response.json().get('mailings_messages')
        count_messages = len(messages_list)
        
        messages = models.Message.objects.all()
        
        self.assertEqual(count_messages, 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            messages_list, serializers.MessageSerializer(messages, many=True).data
            )
        