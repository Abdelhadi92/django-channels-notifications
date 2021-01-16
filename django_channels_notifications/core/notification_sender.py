from django.db.models import QuerySet

class NotificationSender:

    # Send the given notification to the given notifiable entities.
    @classmethod
    def send(cls, notifiables, notification, channels=None):
        cls.send_now(notifiables, notification, channels)

    # Send the given notification immediately.
    @classmethod
    def send_now(cls, notifiables, notification, channels=None):
        notifiables = cls.format_notifiables(notifiables)

        for notifiable in notifiables:
            via_channels = channels
            if not channels:
                via_channels = notification.via(notifiable)
            if not via_channels:
                continue

            for channel in via_channels:
                cls.send_to_notifiable(notifiable, notification, channel)

    # Format the notifiables into a Collection / array if necessary.
    @classmethod
    def send_to_notifiable(cls, notifiable, notification, channel):

        if notifiable.should_send_notification(notification, channel):
            channel().send(notifiable, notification)

    # Format the notifiables into a Collection / array if necessary.
    @classmethod
    def format_notifiables(cls, notifiables):
        if not isinstance(notifiables, QuerySet):
            return [notifiables]
        return notifiables
