from . import models
from django.db.models import Count
from typing import List, Dict
import datetime 


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


def get_phones_for_mailing(tag: str) -> List[Dict]:
    phones = models.Client.objects.filter(tag=tag).values('phone')
    return list(phones)


def get_text_message(id: int) -> dict:
    try:
        message = models.Mailing.objects.get(id=id)
        return {"text": message.text}
    except models.Mailing.DoesNotExist:
        # TODO add logging
        print('exception')
        

def create_object_to_send(id: int, tag: str) -> List[Dict]:
    """
    Creates a list of objects that will be sent to mailing service
    """
    message = get_text_message(id)
    phones = get_phones_for_mailing(tag)
    data = []
    for obj in phones:
        obj.setdefault('text', message)
        obj.setdefault('id', id)
        data.append(obj)
    return data

def check_time(id: int):
    """
    Gets the mailing by id and checks:
        if time start < current time < finish time
    """
    mailing = models.Mailing.objects.get(id=id)
    time_start = mailing.date_start
    time_finish = mailing.date_finish
    current_datetime = datetime.datetime.now()
    if time_start < current_datetime < time_finish:
        print('start')