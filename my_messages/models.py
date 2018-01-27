from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from channels import Group

import json

class League(models.Model):
    """
    Corresponds to room/group
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    league = models.ForeignKey(League, related_name='messages', on_delete=models.CASCADE)
    handle = models.TextField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '<Message("{}") by {} in {}>'.format(self.message,
                                                    self.handle,
                                                    self.league.name)

    def as_json(self):
        """
        return json string
        """
        rep = {
                'handle': self.handle,
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
