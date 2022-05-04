from enum import IntEnum


class MessageType(IntEnum):
    CREATE = 0
    SPAWN = 1
    MOVE = 2
    PICKUP = 3
    PUTINPLACE = 4
    DOACTIVITY = 5