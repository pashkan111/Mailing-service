from . import models
from django.db.models import Count
from typing import List, Dict
import datetime
from utils.logger import get_logger


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


def check_time(id: int) -> bool:
    """
    Gets the mailing by id and checks:
        if time start < current time < finish time returns True
    """
    mailing = models.Mailing.objects.get(id=id)
    time_start = mailing.date_start
    time_finish = mailing.date_finish
    current_datetime = datetime.datetime.now()
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

    def _get_text_message(self) -> dict:
        try:
            message = models.Mailing.objects.get(id=self.id)
            return {"text": message.text}
        except models.Mailing.DoesNotExist as e:
            logger.error(str(e))
        
    def _create_object_to_send(self) -> List[Dict]:
        """
        Creates a list of objects that will be sent to mailing service
        """
        message = self._get_text_message()
        phones = self._get_phones_for_mailing()
        data = []
        for obj in phones:
            obj.setdefault('text', message)
            obj.setdefault('id', id)
            data.append(obj)
        logger.info('Data collected', data)
        return data
        
        
