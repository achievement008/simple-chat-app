from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

from simplechat.main.utils import update_user, save_message


class ChatConsumer(JsonWebsocketConsumer):

    def connect(self):
        """
        Accept new connections and add user at chat_root group
        """
        async_to_sync(self.channel_layer.group_add)(
            'chat_room',
            self.channel_name,
        )
        self.accept()

    def receive_json(self, content, **kwargs):
        """
        Called when consumer receive json
        """
        message_type = content.get("type", None)

        update_user(content['username'])

        if message_type == "join":
            self.join(content['username'])
        elif message_type == "send_message":
            self.send_mess(content["message"], content['username'])
        elif message_type == "typing":
            self.typing(content["username"])

    def join(self, username):
        """
        Called when someone join chat.
        """
        async_to_sync(self.channel_layer.group_send)(
            'chat_room',
            {
                "type": "chat.join",
                "username": username,
            }
        )

    def send_mess(self, message, username):
        """
        Called when someone sends message to chat.
        """
        async_to_sync(self.channel_layer.group_send)(
            'chat_room',
            {
                "type": "chat.message",
                "username": username,
                "message": message,
            }
        )

    def typing(self, username):
        """
        Called when someone typing.
        """
        async_to_sync(self.channel_layer.group_send)(
            'chat_room',
            {
                "type": "chat.typing",
                "username": username,
            }
        )

    def chat_message(self, event):
        """
        Called when someone has messaged.
        """
        save_message(text=event['message'], username=event['username'])
        self.send_json(
            {
                "username": event["username"],
                "message": event["message"],
                "msg_type": "message"
            },
        )

    def chat_typing(self, event):
        """
        Called when someone typing.
        """
        self.send_json(
            {
                "msg_type": 'typing',
                "username": event['username'],
            },
        )

    def chat_join(self, event):
        """
        Called when someone has joined.
        """
        self.send_json(
            {
                "msg_type": 'join',
                "username": event["username"],
            },
        )

    def chat_stats(self, event):
        """
        Send stats to clients.
        """
        self.send_json(
            {
                "msg_type": 'stats',
                "stats": event['stats'],
            },
        )
