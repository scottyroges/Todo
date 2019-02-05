from enum import Enum


class HabitBufferType(Enum):
    DAY_START = "day_start",
    HOURS = "hours"


class HabitBuffer:
    def __init__(self,
                 buffer_type: HabitBufferType,
                 amount):
        self.buffer_type = buffer_type
        self.amount = amount
