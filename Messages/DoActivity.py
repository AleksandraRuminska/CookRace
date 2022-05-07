from Messages.Message import Message
from Messages.MessageType import MessageType


class DoActivity(Message):
    def __init__(self, id, time):
        self._messageType = MessageType.DOACTIVITY
        self._id = id
        self._time = time

    def encode(self):
        arr = [self._messageType, self._id, self._time]
        return self.convertArr(arr)

    def get_time(self):
        return self._time

    def get_message_type(self):
        return self._messageType
