import json
from urllib.parse import parse_qs

from django.contrib.auth.models import User
from channels import Group
from channels.sessions import http_session
from channels.auth import channel_session_user, channel_session_user_from_http

from my_messages.models import League, Message

@channel_session_user
def ws_receive(message):
    room_name = message.content['path'].strip('/').replace('/', '-')
    league = League.objects.get(name=room_name)
    Message.objects.create(
        league=league,
        handle=message.user.username,
        message=message.content['text']
        )

@channel_session_user_from_http
def ws_add(message):
    print(message.user)
    room_name = message.content['path'].strip('/').replace('/', '-')
    message.reply_channel.send({'accept': True})
    Group(room_name).add(message.reply_channel)

@channel_session_user
def ws_disconnect(message):
    room_name = message.content['path'].strip('/').replace('/', '-')
    Group(room_name).discard(message.reply_channel)
