import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from channels import Group

from storage.utils import message_websocket_json

def sentient_user():
    User = get_user_model()
    return User.objects.get_or_create(username='default_user')[0]

class League(models.Model):
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     through="Membership",
                                     related_name="member_of")
    
    def __str__(self):
        return self.name

class Membership(models.Model):
    PERMISSIONS = (
        ('4', 'owner'),
        ('3', 'master'),
        ('2', 'member'),
        ('1', 'guest')
    )
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    permissions = models.CharField(max_length=1,
                                   choices=PERMISSIONS,
                                   default='2')
    joined_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return '{} in {}'.format(self.user, self.league)
    
    def can_send(self):
        return self.permissions != '1'
    
    def can_kick(self):
        print(self.permissions)
        return self.permissions in ['4', '3']

class Message(models.Model):
    league = models.ForeignKey(League, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,
                               default=1,
                               on_delete=models.SET(sentient_user))
    message = models.TextField()
    previous_message = models.OneToOneField(
        'self',
        null=True,
        on_delete=models.SET_NULL,
        related_name="next_message")
    sent_at = models.DateTimeField(auto_now=True)

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
                'sent_at': self.sent_at.strftime('%b %m %Y, %H:%M %p'),
            }
        return json.dumps(rep)

@receiver(post_save, sender=Message)
def send_msg_with_websocket(sender, instance, created, **kwargs):
    if created:
        Group(instance.league.slug).send({
            'text': message_websocket_json(instance),
        })

class Invite(models.Model):
    PERMISSIONS = (
        ('4', 'owner'),
        ('3', 'master'),
        ('2', 'member'),
        ('1', 'guest')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    permissions = models.CharField(max_length=1,
                                   choices=PERMISSIONS,
                                   default='2')
    sent_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ("user", "league",)