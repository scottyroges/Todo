from enum import Enum


class ReoccurRepeatType(Enum):
    DAY_OF_WEEK = "day_of_week",
    DAY_OF_MONTH = "day_of_month"


class ReoccurRepeat:
    def __init__(self,
                 repeat_type: ReoccurRepeatType,
                 when):
        self.repeat_type = repeat_type
        self.when = when
        # TODO: need to figure out if when has a type
