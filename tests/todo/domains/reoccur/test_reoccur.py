import datetime

from freezegun import freeze_time

from app.todo.domains.action import Action
from app.todo.domains.category import Category
from app.todo.domains.reoccur.reoccur import Reoccur
from app.todo.domains.reoccur.reoccur_repeat import ReoccurRepeat, ReoccurRepeatType
from app.todo.domains.tag import Tag
from app.todo.domains.todo_owner import TodoOwner


@freeze_time("2019-02-24 10:00:04")
def test_to_dict():
    todo_owner = TodoOwner(owner_id="123")
    repeat = ReoccurRepeat(repeat_type=ReoccurRepeatType.DAY_OF_WEEK,
                           when=["Sunday"])
    categories = [Category(name="test"), Category(name="again")]
    tags = [Tag(name="who"), Tag(name="knows")]
    actions = [Action(points=2)]
    reoccur = Reoccur(todo_id="abc",
                      todo_owner=todo_owner,
                      name="reoccur",
                      description="description",
                      completion_points=1,
                      required=False,
                      repeat=repeat,
                      categories=categories,
                      tags=tags,
                      actions=actions)

    assert reoccur.to_dict() == {
        "todoId": "abc",
        "todoOwnerId": "123",
        "name": "reoccur",
        "description": "description",
        "todoType": "REOCCUR",
        "completionPoints": 1,
        "required": False,
        "repeat": {
            "repeatType": "DAY_OF_WEEK",
            "when": ["Sunday"],
        },
        "categories": ["test", "again"],
        "tags": ["who", "knows"],
        "createdDate": datetime.datetime(2019, 2, 24, 10, 0, 4),
        "modifiedDate": datetime.datetime(2019, 2, 24, 10, 0, 4),
        "actions": [{
            "actionDate": datetime.datetime(2019, 2, 24, 10, 0, 4),
            "points": 2
        }]
    }
