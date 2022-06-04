from Messages.Message import Message
from Messages.enums.MessageType import MessageType


class Face(Message):
    def __init__(self, id, direction):
        self._messageType = MessageType.FACE
        self._id = id
        self._direction = direction

    def encode(self):
        arr = [self._messageType, self._id, self._direction]
        return self.convertArr(arr)
