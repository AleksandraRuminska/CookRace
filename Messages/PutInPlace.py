from Messages.Message import  Message
from Messages.enums.MessageType import MessageType


class PutInPlace(Message):
    def __init__(self, id, x_s, x_r, y_s, y_r):
        self._messageType = MessageType.PUTINPLACE
        self._id = id
        self._x_s = x_s
        self._x_r = x_r
        self._y_s = y_s
        self._y_r = y_r
        # print("X init put place: ", self._x_s, " ", self._x_r)
        # print("Y init put place: ", self._y_s, " ", self._y_r)

    def encode(self):
        arr = [self._messageType, self._id, self._x_s, self._x_r, self._y_s, self._y_r]
        # print("X: ", self._x_s, " ", self._x_r)
        # print("Y: ", self._y_s, " ", self._y_r)
        return self.convertArr(arr)

