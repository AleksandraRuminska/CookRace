from enum import IntEnum


class MessageType(IntEnum):
    CREATE = 0
    PUTINPLACE = 1
    MOVE = 2
    PICKUP = 3
    DOACTIVITY = 4
    FACE = 5
    POINTS = 6
