from enum import IntEnum


class MessageType(IntEnum):
    CREATE = 0
    PUTINPLACE = 1
    MOVE = 2
    PICKUP = 3
