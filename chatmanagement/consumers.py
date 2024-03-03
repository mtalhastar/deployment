import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

from chatmanagement.models import Message, UserProfile

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sender_id = self.scope['url_route']['kwargs']['sender_id']
        self.receiver_id = self.scope['url_route']['kwargs']['receiver_id']
        self.room_name = self.get_room_name(self.sender_id, self.receiver_id)

        # Join room
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['content']
         
         
        
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "chat_message",
                "content": message,
                "senderid": self.sender_id,
                "receiverid": self.receiver_id,
                "seen":True
            }
        )

    async def chat_message(self, event):
        message = event['content']
        sender_id = event['senderid']
        receiverid =  event['receiverid']
        flag =   event['seen']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "content": message,
                "senderid": sender_id,
                "receiverid": receiverid,
                "seen":flag
        }))

    @staticmethod
    def get_room_name(sender_id, receiver_id):
        # Ensure the room name is consistent regardless of sender and receiver order
        return f"chat_{min(sender_id, receiver_id)}_{max(sender_id, receiver_id)}"
