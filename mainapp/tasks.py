from celery import shared_task


@shared_task
def check_mailing_time():
    """
    Got run right after creating new mailing
    and check the time
    """
    pass