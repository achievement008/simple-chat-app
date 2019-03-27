import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from simplechat.main.models import Message, Member

channel_layer = get_channel_layer()

logger = logging.getLogger('celery')


def send_chat_stats(stats):
    async_to_sync(channel_layer.group_send)(
        'chat_room',
        {
            "type": "chat.stats",
            "stats": stats,
        }
    )


def save_message(**kwargs):
    user, _ = Member.objects.get_or_create(username=kwargs['username'])
    Message.objects.create(text=kwargs['text'], user_id=user.id)


def update_user(username):
    try:
        member = Member.objects.get(username=username)
    except Member.DoesNotExist:
        pass
    else:
        member.save()
