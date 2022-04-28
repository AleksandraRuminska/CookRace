from Messages.Message import  Message
from Messages.MessageType import MessageType


class PickUp(Message):
    def __init__(self, id,pickingUp = 0):
        self._messageType = MessageType.PICKUP
        self._id = id
        self._pickingUp = pickingUp

    def encode(self):
        arr = [self._messageType, self._id, self._pickingUp]
        byteArr = [x.to_bytes(1, byteorder='big', signed=True) for x in arr]
        return byteArr
