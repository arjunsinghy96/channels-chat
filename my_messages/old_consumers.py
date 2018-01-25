import json
from urllib.parse import parse_qs

from channels import Group
from channels.sessions import channel_session

from my_messages.models import League, Message

@channel_session
def ws_receive(message):
    room_name = message.content['path'].strip('/').replace('/', '-')
    print(message)
    league = League.objects.get(name=room_name)
    Message.objects.create(
        league=league,
        handle=message.channel_session['username'],
        message=message.content['text']
        )

@channel_session
def ws_add(message):
    room_name = message.content['path'].strip('/').replace('/', '-')
    message.reply_channel.send({'accept': True})
    params = parse_qs(message.content['query_string'])
    if b'username' in params:
        message.channel_session['username'] = params[b'username'][0].decode('utf8')
        Group(room_name).add(message.reply_channel)
    else:
        message.reply_channel.send({'close': True})

@channel_session
def ws_disconnect(message):
    room_name = message.content['path'].strip('/').replace('/', '-')
    Group(room_name).discard(message.reply_channel)
