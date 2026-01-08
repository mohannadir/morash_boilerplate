from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from django.contrib.auth import get_user_model

def send_to_channel_group_sync(group: str, action: str, payload_data: dict, page_id: str = 'all_pages'):
    """ Send a message to a channel group synchronously.

        :param group: The group to send the message to.
        :type group: str
        :param action: The action to send.
        :type action: str
        :param payload_data: The data to send.
        :type payload_data: dict
        :param page_id: The page ID to send the message to. Default is 'all_pages'.
        :type page_id: str
        :return: None
        :rtype: None
    """
    
    channel_layer = get_channel_layer()
    data = {
        'type' : 'send_message',
        'action' : action,
        'page_id' : page_id,
        'payload' : payload_data
    }
    
    async_to_sync(channel_layer.group_send)(
        group,
        data
    )

async def send_to_channel_group_async(group: str, action: str, payload_data: dict, page_id: str = 'all_pages'):
    """ Send a message to a channel group asynchronously.

        :param group: The group to send the message to.
        :type group: str
        :param action: The action to send.
        :type action: str
        :param payload_data: The data to send.
        :type payload_data: dict
        :param page_id: The page ID to send the message to. Default is 'all_pages'.
        :type page_id: str
        :return: None
        :rtype: None
    """

    channel_layer = get_channel_layer()
    data = {
        'type' : 'send_message',
        'action' : action,
        'page_id' : page_id,
        'payload' : payload_data
    }
    await channel_layer.group_send(
        group,
        data
    )

def send_websocket_message_to_user(user:get_user_model, action: str, payload_data: dict, page_id: str = 'all_pages') -> None:
    """ Send a message to a user. 
    
        :param user: The user to send the message to.
        :type user: User
        :param action: The action to send.
        :type action: str
        :param payload_data: The data to send.
        :type payload_data: dict
        :param page_id: The page ID to send the message to. Default is 'all_pages'.
        :type page_id: str
        :return: None
        :rtype: None
    """
    
    channel_layer = get_channel_layer()
    data = {
        'type' : 'send_message',
        'action' : action,
        'page_id' : page_id,
        'payload' : payload_data
    }
    
    async_to_sync(channel_layer.group_send)(
        f'user_{user.id}',
        data
    )