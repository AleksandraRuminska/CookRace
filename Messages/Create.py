from Messages.Message import Message
from Messages.enums.MessageType import MessageType


class Create(Message):
    def __init__(self, id, controlling):
        self._messageType = MessageType.CREATE
        self._id = id
        self._controlling = controlling

    def encode(self):
        arr = [self._messageType, self._id, self._controlling]

        return self.convertArr(arr)
