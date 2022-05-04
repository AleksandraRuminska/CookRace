from Messages.Message import Message
from Messages.MessageType import MessageType


class Create(Message):
    def __init__(self, id, controlling):
        self._messageType = MessageType.CREATE
        self._id = id
        self._controlling = controlling

    def encode(self):
        arr = [self._messageType, self._id, self._controlling]
        byteArr = [x.to_bytes(1, byteorder='big', signed=True) for x in arr]
        return byteArr