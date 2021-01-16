from abc import ABC, abstractmethod


class BaseChannel(ABC):

    # Send the given notification to the given notifiable entities.
    @abstractmethod
    def send(self, notifiable, notification):
        pass
