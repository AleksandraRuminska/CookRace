from Messages import ActivityType
from Messages.Message import Message
from Messages.MessageType import MessageType


class DoActivity(Message):
    def __init__(self, id, time, activityType = ActivityType.ActivityType.MOVE_R):
        self._messageType = MessageType.DOACTIVITY
        self._id = id
        self._time = time
        self._activityType = activityType

    def encode(self):
        arr = [self._messageType, self._id, self._time]
        return self.convertArr(arr)

    def get_time(self):
        return self._time

    def get_message_type(self):
        return self._messageType

    def get_activity_type(self):
        return self._activityType