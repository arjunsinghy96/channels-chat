import json

from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from channels import Group

from my_messages.models import League
from . import utils

class Message(models.Model):
    league = models.ForeignKey(League, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User,
                               default=1,
                               on_delete=models.SET(utils.sentient_user))
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '<Message("{}") by {} in {}>'.format(self.message,
                                                    self.sender.username,
                                                    self.league.name)

    def as_json(self):
        """
        return json string
        """
        rep = {
                'handle': self.sender.username,
                'message': self.message,
                'timestamp': self.timestamp.strftime('%b %m %Y, %H:%M %p'),
            }
        return json.dumps(rep)


@receiver(post_save, sender=Message)
def send_msg_with_websocket(sender, instance, created, **kwargs):
    if created:
        Group(instance.league.name).send({
            'text': instance.as_json(),
            })
