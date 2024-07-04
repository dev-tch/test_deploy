from channels.generic.websocket import AsyncWebsocketConsumer
import json

class CounterConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('counter_group', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('counter_group', self.channel_name)

    async def counter_update(self, event):
        counter = event['counter']
        ref_office = event['ref_office']
        await self.send(text_data=json.dumps({
            'counter': counter,
            'ref_office': ref_office
        }))
