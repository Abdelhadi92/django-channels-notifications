from django_channels_notifications.core.channels.base_channel import BaseChannel
from django.core.mail import EmailMessage, EmailMultiAlternatives


class MailChannel(BaseChannel):

    # Send the given notification.
    def send(self, notifiable, notification):
        message = self.get_message(notifiable, notification)
        message.send()

    # Get the message for the notification.
    def get_message(self, notifiable, notification):
        if hasattr(notification, 'to_mail'):
            message = notification.to_mail(notifiable)
            if not (isinstance(message, EmailMessage) or isinstance(message, EmailMultiAlternatives)):
                raise Exception("The to_mail method should be return instance of EmailMessage or EmailMultiAlternatives")
            return message
        raise Exception("Notification is missing to_mail method.")


