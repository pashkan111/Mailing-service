from operator import mod
from celery import shared_task
from .services import send_data
from mainapp.mailing_service.client import ServiceClient
from utils.logger import get_logger
from . import models


logger = get_logger(__name__)

@shared_task
def check_mailing_time(id: int):
    """
    Got run right after creating new mailing.
    Checks the time of mailing and if is satisfies condition - 
    sends data
    """
    mailing = models.Mailing.objects.get(id=id)
    response = send_data(mailing)
    if not response:
        logger.info(
            f'The mailing with id = {id} has not been sent'
        )
    else:
        logger.info(
            f'The mailing with id = {id} has delivered'
        )
        

@shared_task
def find_mailings_to_run():
    """
    Every minute finds all mailings that should be run now
    """
    all_mailings = models.Mailing.objects.filter(is_sent=False)
    for mailing in all_mailings:
        response = send_data(mailing)
        if not response:
            logger.info(
            f'The mailing with id = {id} has not been sent'
        )
        else:
            logger.info(
                f'The mailing with id = {id} has delivered'
            )

