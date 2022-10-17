from channels.generic.websocket import AsyncWebsocketConsumer
import json
import time

class SubmissionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['task_id']
        print(self.room_name)
        self.room_group_name = 'submission_%s' % self.room_name
        print(self.room_group_name)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['response']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'submission_message',
                'response': message
            }
        )

    # Receive message from room group
    async def submission_message(self, event):
        message = event['response']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'response': message
        }))


class GraphQLTaskStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = '-'.join(self.scope['url_route']['kwargs']['task_id'].split('_'))
        # self.room_name = 'graphql_room'
        print(self.room_name)
        self.room_group_name = 'graphqltaskstatus-%s' % self.room_name
        # self.room_group_name = 'graphql_group_room'
        print(self.room_group_name)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['response']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'graphql_task_result',
                'response': message
            }
        )

    # Receive message from room group
    async def graphql_task_result(self, event):
        message = event['response']
        print(message)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'response': message
        }))
