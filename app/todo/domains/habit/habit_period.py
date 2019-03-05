from enum import Enum


class HabitPeriodType(Enum):
    DAYS = "days"
    WEEKS = "weeks"
    MONTHS = "months"
    YEARS = "years"


class HabitPeriod:
    def __init__(self,
                 period_type: HabitPeriodType,
                 amount=None):
        self.period_type = period_type
        # making this always one for now
        # it simplifies the is complete part
        self.amount = 1
