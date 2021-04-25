from celery import shared_task

from .currency_services import parse_monobank, parse_vkurse, parse_yahoo


@shared_task
def parse_currencies():
    parse_monobank()
    parse_vkurse()
    parse_yahoo()
