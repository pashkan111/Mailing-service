from . import models
from django.db.models import Count
from typing import List, Dict
import datetime
from utils.logger import get_logger
import pytz


logger = get_logger(__name__)


def get_statistic() -> dict:
    """
    Get count of messages for each mailing grouped by status
    """
    all_mailings = models.Mailing.objects.all()
    messages = {}
    for mail in all_mailings:
        mail_message = list(mail.mailings_messages.all().values('status').annotate(total=Count('id')))
        messages.setdefault(mail.id, mail_message)
    return messages


def check_time(time_start: datetime, time_finish: datetime) -> bool:
    """
    Checks if time start < current time < finish time returns True
    """
    from django.utils.timezone import utc
    current_datetime = datetime.datetime.utcnow().replace(tzinfo=utc)
    if time_start < current_datetime < time_finish:
        return True
    return False


class MailingData:
    def __init__(self, id: int, tag: str):
        self.tag = tag
        self.id = id
        self.data = self._create_object_to_send()
        
    def _get_phones_for_mailing(self) -> List[Dict]:
        phones = models.Client.objects.filter(tag=self.tag).values('phone')
        return list(phones)

    def _get_text_message(self) -> str:
        try:
            message = models.Mailing.objects.get(id=self.id)
            return message.text
        except models.Mailing.DoesNotExist as e:
            logger.error(str(e))
        
    def _create_object_to_send(self) -> List[Dict]:
        """
        Creates a list of objects that will be sent to mailing service
        """
        text = self._get_text_message()
        phones = self._get_phones_for_mailing()
        data = []
        for obj in phones:
            obj.setdefault('text', text)
            obj.setdefault('id', self.id)
            data.append(obj)
        logger.info('Data collected')
        logger.info(data)
        return data
        
        
def get_clients(data: dict):
    data_copied = data.copy()
    # Removing clients with delivery error
    for phone, result in data.items():
        if result == False:
            del data_copied[phone]
            
    phones = data_copied.keys()
    clients = models.Client.objects.filter(
        phone__in=phones
    )
    return clients


def create_message_for_statistic(
    clients: models.Client, mailing: models.Mailing
    ):

    for client in clients:
        models.Message.objects.create(
            status=models.Message.DELIVERED,
            mailing=mailing,
            client_to=client
        )
        
    
    