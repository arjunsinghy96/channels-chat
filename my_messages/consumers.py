from channels.generic.websockets import WebsocketConsumer
from channels import Group

from my_messages.models import League, Message

class websockets(WebsocketConsumer):

    http_user = True

    def connection_groups(self, **kwargs):
        """
        Returns the list of groups a connection is to be added.
        """
        return ['all_notify'] # a common group for every websocket

    def connect(self, message, **kwargs):
        """
        Run when a new websocket is connected
        """
        self.room = self.path.strip('/').split('/')[-1]
        Group(self.room).add(message.reply_channel)
        message.reply_channel.send({'accept': True})

    def receive(self, text=None, bytes=None, **kwargs):
        """
        Actions on receiving a message on websocket.
        Save the Message with appropriate League and message
        """
        self.room = self.path.strip('/').split('/')[-1]
        league = League.objects.get(name=self.room)
        m = Message.objects.create(
                league=league,
                sender=self.message.user,
                message=text,
                )

    def disconnect(self, message, **kwargs):
        """
        Run when a socket is disconnected
        """
        self.room = self.path.strip('/').split('/')[-1]
        Group(self.room).discard(message.reply_channel)
