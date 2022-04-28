from Messages.Message import  Message
from Messages.MessageType import MessageType


class Spawn(Message):
    def __init__(self, id, x, y, controlling):
        self._messageType = MessageType.SPAWN
        self._id = id
        self._X = x
        self._Y = y
        self._controlling = controlling

    def encode(self):
        arr = [self._messageType, self._id, self._X, self._Y, self._controlling]
        byteArr = [x.to_bytes(1, byteorder='big', signed=True) for x in arr]
        return byteArr
