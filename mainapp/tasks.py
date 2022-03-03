from celery import shared_task
from .services import check_time, MailingData
from mainapp.mailing_service.client import ServiceClient
from utils.logger import get_logger


logger = get_logger(__name__)

@shared_task
def check_mailing_time(id: int, tag: str):
    """
    Got run right after creating new mailing.
    Checks the time of mailing and if is satisfies condition - 
    sends data
    """
    is_started = check_time(id)
    if is_started:
        data = MailingData(id, tag)
        client = ServiceClient(data.data)
        client.send_data()
    else:
        logger.info(
            f'The mailing with id = {id} does not satisfy time condition'
            )