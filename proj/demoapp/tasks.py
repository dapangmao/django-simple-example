from __future__ import absolute_import
from celery import shared_task
import requests


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def count_words_at_url():
    resp = requests.get('http://www.mitbbs.com')
    return len(resp.text.split())
