from enum import Enum


class HabitPeriodType(Enum):
    DAYS = "days"
    HOURS = "hours"
    WEEKS = "weeks"
    MONTHS = "months"


class HabitPeriod:
    def __init__(self,
                 period_type: HabitPeriodType,
                 amount,
                 start):
        self.period_type = period_type
        self.amount = amount
        self.start = start
