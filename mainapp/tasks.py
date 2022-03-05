from operator import mod
from celery import shared_task
from .services import check_time, MailingData
from mainapp.mailing_service.client import ServiceClient
from utils.logger import get_logger
from . import models


logger = get_logger(__name__)

@shared_task
def check_mailing_time(id: int, tag: str):
    """
    Got run right after creating new mailing.
    Checks the time of mailing and if is satisfies condition - 
    sends data
    """
    mailing = models.Mailing.objects.get(id=id)
    is_started = check_time(
        mailing.time_start,
        mailing.time_finish
    )
    if is_started:
        data = MailingData(id, tag)
        client = ServiceClient(data.data)
        client.send_data()
        mailing.is_sent = True
        mailing.save()
    else:
        logger.info(
            f'The mailing with id = {id} does not satisfy time condition'
            )


@shared_task
def find_mailings_to_run():
    """
    Every minute finds all mailings that should be run now
    """
    all_mailings = models.Mailing.objects.filter(is_sent=False)
    for mailing in all_mailings:
        is_started = check_time(
            mailing.time_start,
            mailing.time_finish
        )
        if is_started:
            data = MailingData(mailing.id, mailing.tag)
            client = ServiceClient(data.data)
            client.send_data()
            mailing.is_sent = True
            mailing.save()
            