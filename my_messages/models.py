from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from channels import Group

import json


def sentient_user():
    return User.objects.get_or_create(username='default_user')[0]

class League(models.Model):
    """
    Corresponds to room/group
    """
    name = models.CharField(max_length=50, unique=True)
    members = models.ManyToManyField(User,
                                     through='Membership',
                                     related_name='member_of')

    def __str__(self):
        return self.name

    def add_member(self, user):
        mem, created = Membership.objects.get_or_create(league=self,
                                                        user=user)


class Membership(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return '{} in {}'.format(self.user, self.league)


class Invite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)


class Message(models.Model):
    league = models.ForeignKey(League, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User,
                               default=sentient_user().pk,
                               on_delete=models.SET(sentient_user))
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
