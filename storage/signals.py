import json

from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from channels import Group

from storage.utils import message_websocket_json
from storage.models import League, Membership, Invite, Notification, Message

@receiver(post_save, sender=Message)
def send_msg_with_websocket(sender, instance, created, **kwargs):
    if created:
        Group(instance.league.slug).send({
            'text': message_websocket_json(instance),
        })

@receiver(post_save, sender=Invite)
def send_new_invite_msg(sender, instance, created, **kwargs):
    if created:
        Group(instance.user.username).send({
            'text': json.dumps({
                'type': 'invite:new',
                'content': {}
            })
        })

@receiver(post_delete, sender=Membership)
def send_delete_membership_ws(sender, instance, **kwargs):
    Group(instance.league.slug).send({
        'text': json.dumps({
            'type': 'league:kicked',
            'content':{
                'member': instance.user.username,
                'league_name': instance.league.name,
                'league_slug': instance.league.slug,
            }
        })
    })
    Group(instance.user.username).send({
        'text': json.dumps({
            'type': 'league:kicked:self',
            'content': {
                'league_name': instance.league.name,
                'league_slug': instance.league.slug,
            }
        })
    })

@receiver(post_save, sender=Notification)
def send_notification_ws(sender, instance, created, **kwargs):
    if created:
        Group('all_notify').send({
            'text': json.dumps({
                'type': 'notify:new',
                'content': {
                    'text': instance.text,
                }
            })
        })