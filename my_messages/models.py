from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels import Group
from django.core.serializers import serialize

import json

class League(models.Model):
    """
    Corresponds to room/group
    """
    name = models.CharField(max_length=50, unique=True)

class Message(models.Model):
    league = models.ForeignKey(League, related_name='messages', on_delete=models.CASCADE)
    handle = models.TextField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

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
