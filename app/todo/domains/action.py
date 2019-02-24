import datetime


class Action:
    def __init__(self,
                 action_id=None,
                 action_date=None,
                 points=0):
        self.action_id = action_id
        self.action_date = action_date or datetime.datetime.now()
        self.points = points

    def to_dict(self):
        return {
            "actionDate": self.action_date,
            "points": self.points
        }
