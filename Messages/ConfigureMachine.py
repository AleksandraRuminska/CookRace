from Messages.Message import Message
from Messages.enums.MessageType import MessageType


class ConfigureMachine(Message):
    def __init__(self, id, intensity, machineType, machineID):
        self._messageType = MessageType.CONFIGURE
        self._id = id
        self.intensity = intensity
        self.machineType = machineType
        self.machineID = machineID

    def encode(self):
        arr = [self._messageType, self._id, self.intensity, self.machineType, self.machineID]
        return self.convertArr(arr)
