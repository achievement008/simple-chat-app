import datetime
import logging
import time

from simplechat.main.models import Member
from simplechat.taskapp.celery import app
from .utils import send_chat_stats

logger = logging.getLogger('celery')


@app.task
def send_user_stats():
    """
    Generates a list of inactive users.
    """
    users = Member.objects.values('username', 'updated').filter(
        updated__gte=datetime.datetime.now() - datetime.timedelta(hours=1))

    afk_users = list(filter(
        lambda active_object: active_object['updated'] <= datetime.datetime.now() - datetime.timedelta(minutes=10),
        users))

    afk_users_list = [i['username'] for i in afk_users]

    send_chat_stats(stats={'afk': afk_users_list})


@app.task(bind=True)
def long_task(self, sec=10):
    print(self.request.id)
    time.sleep(sec)
    return sec


@app.task(soft_time_limit=00)
def comp(*args, **kwargs):
    return sum(*args)
