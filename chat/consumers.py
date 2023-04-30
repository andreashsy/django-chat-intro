import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()


    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        print('Message received: ', text_data_json)
        message = text_data_json['message']
        user_id = text_data_json['userId']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message,
                'userId': user_id
            }
        )

    def chat_message(self, event):
        message = event['message']
        user_id = event['userId']

        self.send(text_data=json.dumps({
            'type':'chat',
            'message':message,
            'userId': user_id
        }))