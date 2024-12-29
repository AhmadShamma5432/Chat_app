import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        @database_sync_to_async
        def check_room_existing(room_name):
            from chat_app.models import ChatRoom
            return ChatRoom.objects.filter(name=room_name).exists()
        
        is_room_exists = await check_room_existing(self.room_name)
        if not is_room_exists:
            await self.close()
            return 
        
        @database_sync_to_async
        def add_participant(room_name,user,is_admin=False):
            from chat_app.models import ChatRoomParticipant,ChatRoom
            room = ChatRoom.objects.get(name = room_name)
            ChatRoomParticipant.objects.create(room=room,user=user)
        
        await add_participant(self.room_name,self.scope['user'])
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type":"user_event",
                "event_tpe":"join",
                "username":self.scope['user'].username
            }
        )

        await self.accept()

    
    async def disconnect(self, code):
        @database_sync_to_async
        def discard_user(room_name,user):
            from chat_app.models import ChatRoom,ChatRoomParticipant
            room = ChatRoom.objects.get(name = room_name)
            ChatRoomParticipant.objects.filter(room=room,user=user).delete()
        
        self.channel_layer.group_send(
            self.room_group_name,
            {
                "type":"user_event",
                "event_type":"leave",
                "username":self.scope['user'].username
            }
        )

        await discard_user(self.room_name,self.scope['user'])
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        @database_sync_to_async
        def add_message(user,room,message):
            from chat_app.models import Message,ChatRoom
            room = ChatRoom.objects.get(name=room)
            Message.objects.create(user=user,room=room,content=message)

        user = self.scope.get('user')
        username = user.username

        await add_message(user,self.room_name,message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "username": event["username"],
        }))
        
    async def user_event(self,event):
        if event['event_type'] == 'join': 
            await self.send(text_data=json.dumps({
                "type":"notification",
                "message":f"the user{event['username']} joined the chat"
            }))
        elif event['event_type'] == 'leave':
            await self.send(text_data=json.dumps({
                "type":"notification",
                "message":f"the user{event['username']} has left the room"
            }))