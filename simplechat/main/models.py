from model_utils.models import TimeStampedModel, SoftDeletableModel

from django.db import models


class Member(TimeStampedModel):
    username = models.CharField(max_length=32, verbose_name='Username')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Member {self.id}: {self.username}'


class Message(TimeStampedModel):
    user = models.ForeignKey(Member, verbose_name='User',
                             related_name='messages',
                             on_delete=models.CASCADE)
    text = models.CharField(max_length=512, verbose_name='Message')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Chat message: {self.created}'
