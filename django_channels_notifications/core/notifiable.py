from django_channels_notifications.models import DatabaseNotification
from django_channels_notifications.core.notification_sender import NotificationSender


class HasDatabaseNotifications:

    # Get the entity's notifications.
    def notifications(self):
        return DatabaseNotification.objects.filter(notifiable=self)

    # Get the entity's read notifications.
    def read_notifications(self):
        return self.notifications().filter(read_at__isnull=False)

    # Get the entity's unread notifications.
    def unread_notifications(self):
        return self.notifications().filter(read_at__isnull=True)


class RoutesNotifications:

    # Send the given notification.
    def notify(self, instance):
        NotificationSender.send(self, instance)

    # Send the given notification immediately.
    def notify_now(self, instance,  channels=None):
        NotificationSender.send_now(self, instance, channels)

    # Determines if the notification can be sent.
    def should_send_notification(self, notification, channel):
        return True


class Notifiable(HasDatabaseNotifications, RoutesNotifications):
    pass
