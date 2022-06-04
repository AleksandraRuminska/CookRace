from Messages.Message import  Message
from Messages.enums.MessageType import MessageType


class PickUp(Message):
    def __init__(self, id, pickingUp = 0):
        self._messageType = MessageType.PICKUP
        self._id = id
        self._pickingUp = pickingUp

    def encode(self):
        arr = [self._messageType, self._id, self._pickingUp]
        return self.convertArr(arr)
