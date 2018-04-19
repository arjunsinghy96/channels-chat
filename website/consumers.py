import json

from channels.generic.websockets import WebsocketConsumer
from channels import Group

from storage.models import League, Message

class websockets(WebsocketConsumer):

    http_user = True

    def connection_groups(self, **kwargs):
        """
        Returns the list of groups a connection is to be added.
        """
        groups = []
        groups.append(kwargs['room'])
        return groups

    def connect(self, message, **kwargs):
        """
        Run when a new websocket is connected
        """
        message.reply_channel.send({'accept': True})

    def receive(self, text=None, bytes=None, **kwargs):
        """
        Actions on receiving a message on websocket.
        Save the Message with appropriate League and message
        """
        data = json.loads(text)
        self.room = self.path.strip('/').split('/')[-1]
        league = League.objects.get(slug=self.room)
        try:
            latest = Message.objects.filter(league=league, sent_at__isnull=False).latest('sent_at')
        except Message.DoesNotExist:
            latest = None
        if data['msg']:
            m = Message.objects.create(
                    league=league,
                    sender=self.message.user,
                    message=data['msg'],
                    previous_message=latest,
                    )
            if data['urgent']:
                print('Urgent msg sent: Will be sent to mobile and email')

    def disconnect(self, message, **kwargs):
        """
        Run when a socket is disconnected
        """
        pass

class dashboardWebsockets(WebsocketConsumer):

    http_user = True

    def connection_groups(self, **kwargs):
        """
        Returns the list of groups a connection is to be added.
        """
        leagues = self.message.user.member_of.only('name').all()
        groups = [league.slug for league in leagues]
        groups.append('all_notify')
        groups.append(self.message.user.username)
        return groups

    def connect(self, message, **kwargs):
        """
        Run when a new websocket is connected
        """
        message.reply_channel.send({'accept': True})

    def receive(self, text=None, bytes=None, **kwargs):
        """
        Actions on receiving a message on websocket.
        Save the Message with appropriate League and message
        """
        pass

    def disconnect(self, message, **kwargs):
        """
        Run when a socket is disconnected
        """
        pass
