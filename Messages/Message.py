from abc import ABC, abstractmethod


class Message(ABC):

    @abstractmethod
    def encode(self):
        pass

    def convertArr(self, arr):
        byteArr = [x.to_bytes(1, byteorder='big', signed=True) for x in arr]
        return b''.join(byteArr) + b'\0' * (6 - len(byteArr))
