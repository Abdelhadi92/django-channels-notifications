from django_channels_notifications.core.channels.base_channel import BaseChannel
from django.conf import settings
import requests


class UnifonicChannel(BaseChannel):
    BASE_URL = "http://api.unifonic.com/"

    # Send the given notification.
    def send(self, notifiable, notification):
        message = self.get_message(notifiable, notification)

        if not message.recipient or not message.body:
            return

        requests.post(
            '{}/rest/Messages/Send'.format(UnifonicChannel.BASE_URL),
            data={
                'AppSid': settings.UNIFONIC_APPSID,
                'Body': message.body,
                'Recipient': message.recipient,
                'Priority': message.priority,
                'SenderID': message.sender_id
              },
            headers={'Content-Type': 'application/x-www-form-urlencoded'})

    # Get the message for the notification.
    def get_message(self, notifiable, notification):
        if hasattr(notification, 'to_unifonic'):
            message = notification.to_unifonic(notifiable)
            if not isinstance(message, UnifonicMessage):
                raise Exception("The to_unifonic method should be return instance of UnifonicMessage")
            return message
        raise Exception("Notification is missing to_unifonic method.")


class UnifonicMessage(object):

    __slots__ = ['sender_id', 'body', 'recipient', 'priority']

    # Create a new message instance.
    def __init__(self, body='', recipient='', sender_id=None, priority=None):
        self.body = body
        self.recipient = recipient
        self.sender_id = sender_id
        self.priority = priority

    # Set the message body.
    def set_body(self, body):
        self.body = body
        return self

    # Set the message recipient.
    def set_recipient(self, recipient):
        self.recipient = recipient
        return self

    # Set the Sender_id the message should be sent from.
    def set_sender_id(self, sender_id):
        self.sender_id = sender_id
        return self

    # Set the message priority to high
    def set_priority(self):
        self.priority = "High"
        return self
