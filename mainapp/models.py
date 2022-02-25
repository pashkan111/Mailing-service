from django.db import models


class Mailing(models.Model):
    """Рассылка"""
    
    date_start = models.DateTimeField()
    date_finish = models.DateTimeField()
    text = models.TextField()
    filter = models.CharField(max_length=250)


class Client(models.Model):
    """Клиент, которому отправляют сообщение"""
    
    phone = models.CharField(max_length=12)
    code = models.CharField(max_length=5)
    timezone = models.CharField(max_length=50)


class Message(models.Model):
    """Сообщение"""
    
    date = models.DateTimeField()
    status = models.CharField(max_length=20)
    mailing = models.ForeignKey(
        Mailing, on_delete=models.SET_NULL, null=True
        )
    client_to = models.ForeignKey(
        Client, on_delete=models.SET_NULL, null=True
        )