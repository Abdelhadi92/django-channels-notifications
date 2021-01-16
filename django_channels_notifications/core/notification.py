from abc import ABC, abstractmethod


class Notification(ABC):

    def __init__(self):
        self.locale = None

    # Get the notification's delivery channels.
    @abstractmethod
    def via(self, notifiable):
        return []

    # Set the locale to send this notification in.
    def locale(self, locale):
        self.locale = locale
        return self
