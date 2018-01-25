from channels import Group
from channels.sessions import channel_session

receivers = []

@channel_session
def ws_add(message):
    message.reply_channel.send({'accept': True})
    print('a new client has connected and if this does not print ..')
    room = message.content['path'].strip('/')
    Group('chat-%s'%room).add(message.reply_channel)
    print(message.content)

@channel_session
def ws_receive(message):
    room = message.content['path'].strip('/')
    Group('chat-%s'%room).send({
        'text': message.content['text']}
        )
