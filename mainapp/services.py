from . import models
from django.db.models import Count
from typing import List, Dict


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
     
     

            
