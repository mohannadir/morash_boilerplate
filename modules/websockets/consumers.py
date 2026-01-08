import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .utils import send_to_channel_group_async

class ShipWithDjangoConsumer(AsyncJsonWebsocketConsumer):
    channel_groups = None

    def get_channel_groups(self):
        if not self.channel_groups:
            raise ValueError('No channel groups defined. Define the channel_groups attribute in the consumer or override the get_channel_groups method.')
        
        formatted_groups = [group.format(user=self.scope['user']) if 'user' in self.scope else group for group in self.channel_groups]
        return formatted_groups
    
    async def connect(self):
        for group in self.get_channel_groups():
            await self.channel_layer.group_add(
                group,
                self.channel_name
            )
        
        await self.accept()
    
    async def disconnect(self, close_code):

        for group in self.get_channel_groups():
            await self.channel_layer.group_discard(
                group,
                self.channel_name
            )
    
    async def receive(self, text_data):
        """
            Receive message from client.
            Get the event and execute the necessary action.
        """
        
        payload = json.loads(text_data)
        event = payload['event'].lower()
        page_id = payload['page_id'] if 'page_id' in payload else 'all_pages'
        user = self.scope['user']

        await self.receive_event(event, page_id, user, payload)
    
    async def receive_event(self, event, page_id, user, response):
        """ Receive an event from the client. """
        
        raise NotImplementedError('You must implement the receive_event method in the consumer.')
       
    async def send_message(self, res):
        """ Send a message to the client. """
        
        action = res['action'].lower()
        page_id = res['page_id']
        payload = res['payload']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "action": action,
            "page_id": page_id,
            "payload": payload
        }))

    async def send_to_all_groups(self, action, payload, page_id='all_pages'):
        """ Send a message to all groups. """

        for group in self.get_channel_groups():
            await send_to_channel_group_async(group, action, payload, page_id)