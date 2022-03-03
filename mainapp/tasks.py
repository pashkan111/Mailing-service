from celery import shared_task
from .services import check_time, MailingData
from mainapp.mailing_service.client import ServiceClient


@shared_task
def check_mailing_time(id: int, tag: str):
    """
    Got run right after creating new mailing.
    Checks the time of mailing and if is satisfies condition - 
    sends data
    """
    is_started = check_time(id, tag)
    if is_started:
        data = MailingData()
        client = ServiceClient(data)
        client.send_data()