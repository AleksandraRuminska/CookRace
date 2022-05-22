from Messages.Message import  Message
from Messages.MessageType import MessageType


class Move(Message):
    def __init__(self, id, dx, dy):
        self._messageType = MessageType.MOVE
        self._id = id
        self._dx = dx
        self._dy = dy

    def encode(self):
        arr = [self._messageType, self._id, self._dx, self._dy]
        return self.convertArr(arr)
