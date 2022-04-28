from abc import ABC, abstractmethod


class Message(ABC):

    @abstractmethod
    def encode(self):
        pass
