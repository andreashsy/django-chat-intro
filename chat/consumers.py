import json
import asyncio
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache

from .services.game_service import RPSGameState
from .models.RPSChoice import RPSChoice
from .models.RPSPlayer import RPSPlayer
from .models.GameResult import GameResult


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'test'
        self.user_id = None

        await (self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
        if not cache.get('game_state'):
            game_state = RPSGameState()
            cache.set('game_state', game_state)

        print(f"{str(datetime.now())} - Group {self.room_group_name} has {len(self.channel_layer.groups.get(self.room_group_name, {}).items())} connection(s)")
        # asyncio.create_task(self.wait_and_send_msg(3))

    async def wait_and_send_msg(self, seconds: int):
        await asyncio.sleep(seconds)

        await (self.channel_layer.group_send)(
        self.room_group_name,
        {
            'type':'chat_message',
            'message':f"{seconds} seconds passed after login!",
            'userId': "Server"
        }
    )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        print(f'{str(datetime.now())} - Message received: ', text_data_json)
        
        msg_type = text_data_json['type']
        message = text_data_json['message']
        user_id = text_data_json['userId']
        if not self.user_id and not msg_type == 'server_message':
            self.user_id = user_id

        if msg_type == 'game_move':
            choice = message
            game_state: RPSGameState = cache.get('game_state')
            user_id = 'Server'
            if not game_state.is_player_waiting():
                game_state.add_player(self.user_id, RPSChoice(choice))
                cache.set('game_state', game_state)
                message = f"{self.user_id} made a game choice!"

            else:
                current_player = RPSPlayer(self.user_id, RPSChoice(choice))
                other_player_id, other_choice = game_state.get_player_details()
                game_result = game_state.resolve_against(current_player)
                if game_result == GameResult.DRAW:
                    message = f"Both {self.user_id} and {other_player_id} chose {choice}! It's a draw!"
                elif game_result == GameResult.WIN:
                    message = f"{other_player_id}'s {other_choice} wins against {self.user_id}'s {choice}!"
                else:
                    message = f"{other_player_id}'s {other_choice} loses against {self.user_id}'s {choice}!"
                game_state.reset()
                cache.set('game_state', game_state)

        await (self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message,
                'userId': user_id
            }
        )

    async def chat_message(self, event):
        message = event['message']
        user_id = event['userId']

        await self.send(text_data=json.dumps({
            'type':'chat',
            'message':message,
            'userId': user_id
        }))

    async def server_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'type':'chat',
            'message':message,
            'userId': "Server"
        }))
    
    async def disconnect(self, code=None):
        print(f'{str(datetime.now())} - {self.user_id} disconnecting!')

        await (self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'server_message',
                'message': f'{self.user_id} has disconnected!',
            }
        )
        await (self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print(f"{str(datetime.now())} - Group <{self.room_group_name}> has {len(self.channel_layer.groups.get(self.room_group_name, {}).items())} connection(s)")
