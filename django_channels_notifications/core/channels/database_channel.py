from django_channels_notifications.core.channels.base_channel import BaseChannel
from django_channels_notifications.models import DatabaseNotification


class DatabaseChannel(BaseChannel):

    # Send the given notification.
    def send(self, notifiable, notification):
        DatabaseNotification(
            type="{0}.{1}".format(notification.__class__.__module__, notification.__class__.__name__),
            notifiable=notifiable,
            data=self.get_data(notifiable, notification)
        ).save()

    # Get the data for the notification.
    def get_data(self, notifiable, notification):
        if hasattr(notification, 'to_database'):
            return notification.to_database(notifiable)

        if hasattr(notification, 'to_dict'):
            return notification.to_dict(notifiable)

        raise Exception("Notification is missing to_database / to_dict method.")






