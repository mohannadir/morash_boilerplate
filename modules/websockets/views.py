from .consumers import ShipWithDjangoConsumer

class ExampleConsumer(ShipWithDjangoConsumer):
    channel_groups = ['examples']

    async def receive_event(self, event, page_id, user, response):

        if event == 'ping':
            await self.send_to_all_groups(
                action='show_message',
                page_id=page_id,
                payload= {
                    'message': 'pong'
                }
            )
        elif event == 'greeting':
            await self.send_to_all_groups(
                action='show_message',
                page_id=page_id,
                payload= {
                    'message': 'Hello, ' + user.get_full_name()
                }
            )
        else:
            await self.send_to_all_groups(
                action='error',
                page_id=page_id,
                payload= {
                    'message': 'Invalid event'
                }
            )

class UserConsumer(ShipWithDjangoConsumer):
    channel_groups = ['users', 'user_{user.id}']

    async def receive_event(self, event, page_id, user, response):
        await self.send_to_all_groups(
            action='error',
            page_id=page_id,
            payload= {
                'message': 'Invalid event'
            }
        )