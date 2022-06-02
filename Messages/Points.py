from Messages.Message import Message
from Messages.MessageType import MessageType


class Points(Message):
    def __init__(self, id, points_hundred, points_rest, sign):
        self._messageType = MessageType.POINTS
        self._id = id
        self._points_hundred = points_hundred
        self._points_rest = points_rest
        self._sign = sign

    def encode(self):
        arr = [self._messageType, self._id,  self._points_hundred, self._points_rest, self._sign]
        return self.convertArr(arr)
