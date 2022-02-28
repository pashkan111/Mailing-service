from django.db import models


class Mailing(models.Model):
    """Рассылка"""
    
    date_start = models.DateTimeField()
    date_finish = models.DateTimeField()
    text = models.TextField()
    filter = models.CharField(max_length=250)
    
    def __str__(self) -> str:
        return self.text


class Client(models.Model):
    """Клиент, которому отправляют сообщение"""
    
    phone = models.CharField(max_length=12)
    code = models.CharField(max_length=5)
    tag = models.CharField(max_length=255, null=True)
    timezone = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return self.phone


class Message(models.Model):
    """Сообщение"""
    
    IN_PROGRESS = 'progress'
    DELIVERED = 'delivered'
    
    STATUS_CHOISES = (
        ('IN_PROGRESS', IN_PROGRESS),
        ('DELIVERED', DELIVERED)
    )
    
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOISES,
        default=IN_PROGRESS
        )
    mailing = models.ForeignKey(
        Mailing, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='mailings_messages'
        )
    client_to = models.ForeignKey(
        Client, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='clients_messages'
        )