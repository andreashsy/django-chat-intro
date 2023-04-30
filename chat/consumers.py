import json
from datetime import datetime
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'
        self.user_id = None

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        print(f"Group {self.room_group_name} has {len(self.channel_layer.groups.get(self.room_group_name, {}).items())} connection(s)")

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        print(f'{str(datetime.now())} - Message received: ', text_data_json)
        message = text_data_json['message']
        user_id = text_data_json['userId']
        if not self.user_id:
            self.user_id = user_id

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
    
    def disconnect(self, code=None):
        print(f'{str(datetime.now())} - {self.user_id} disconnecting!')

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message': 'Disconnected!',
                'userId': self.user_id
            }
        )
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print(f"Group {self.room_group_name} has {len(self.channel_layer.groups.get(self.room_group_name, {}).items())} connection(s)")