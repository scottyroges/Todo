import datetime

from freezegun import freeze_time
from app.model import (
    Reoccur as ReoccurRecord,
    Category as CategoryRecord,
    Tag as TagRecord,
    Action as ActionRecord
)
from app.todo.domains.reoccur.reoccur_repeat import ReoccurRepeat, ReoccurRepeatType
from app.todo.domains.todo_owner import TodoOwner
from app.todo.domains.category import Category as DomainCategory
from app.todo.domains.tag import Tag as DomainTag
from app.todo.domains.action import Action as DomainAction
from app.todo.domains.reoccur.reoccur import Reoccur as DomainReoccur
from app.todo.domains.todo_type import TodoType
from app.todo.transformers.reoccur_transformer import ReoccurTransformer


@freeze_time("2019-02-24")
def test_to_record():
    todo_owner = TodoOwner(owner_id="123")
    repeat = ReoccurRepeat(repeat_type=ReoccurRepeatType.DAY_OF_WEEK,
                           when=["Sunday"])
    tags = [DomainTag(name="who"), DomainTag(name="knows")]
    actions = [DomainAction()]
    reoccur = DomainReoccur(todo_id="abc",
                            todo_owner=todo_owner,
                            name="reoccur",
                            description="description",
                            completion_points=1,
                            required=False,
                            repeat=repeat,
                            category=DomainCategory(category_id="abc",
                                                    name="test",
                                                    color="#FFF"),
                            tags=tags,
                            actions=actions)

    reoccur_record = ReoccurTransformer.to_record(reoccur)

    assert reoccur_record.todo_id == reoccur.todo_id
    assert reoccur_record.todo_owner_id == reoccur.todo_owner.owner_id
    assert reoccur_record.name == reoccur.name
    assert reoccur_record.description == reoccur.description
    assert reoccur_record.completion_points == reoccur.completion_points
    assert reoccur_record.required == reoccur.required
    assert reoccur_record.repeat == {
        'when': ["Sunday"],
        'repeatType': 'DAY_OF_WEEK'
    }
    assert reoccur_record.category_id == "abc"
    for tag_record in reoccur_record.tags:
        tag = filter(lambda x: x.name == tag_record.name, reoccur.tags)
        assert tag is not None
    assert reoccur_record.actions[0].points == reoccur.actions[0].points
    assert reoccur_record.actions[0].action_date == reoccur.actions[0].action_date
    assert reoccur_record.created_date == reoccur.created_date
    assert reoccur_record.modified_date == reoccur.modified_date


def test_from_record():
    repeat = {
        'when': ["Sunday"],
        'repeatType': 'DAY_OF_WEEK'
    }
    tags = [TagRecord(name="who"), TagRecord(name="knows")]
    actions = [ActionRecord(action_date=datetime.datetime(2019, 2, 24),
                            points=1)]
    reoccur_record = ReoccurRecord(todo_id="abc",
                                   todo_owner_id="123",
                                   name="reoccur",
                                   description="description",
                                   todo_type=TodoType.REOCCUR,
                                   completion_points=1,
                                   required=False,
                                   repeat=repeat,
                                   category=CategoryRecord(id="abc",
                                                           name="test",
                                                           color="#FFF"),
                                   tags=tags,
                                   actions=actions,
                                   created_date=datetime.datetime(2019, 2, 24),
                                   modified_date=datetime.datetime(2019, 2, 24))

    reoccur = ReoccurTransformer.from_record(reoccur_record)

    assert reoccur.todo_id == reoccur_record.todo_id
    assert reoccur.todo_owner.owner_id == reoccur_record.todo_owner_id
    assert reoccur.name == reoccur_record.name
    assert reoccur.description == reoccur_record.description
    assert reoccur.completion_points == reoccur_record.completion_points
    assert reoccur.required == reoccur_record.required
    assert reoccur.repeat.when == ["Sunday"]
    assert reoccur.repeat.repeat_type == ReoccurRepeatType.DAY_OF_WEEK
    assert reoccur.category.category_id == "abc"
    assert reoccur.category.name == "test"
    assert reoccur_record.category.color == "#FFF"
    for tag in reoccur.tags:
        tag_record = filter(lambda x: x.name == tag.name, reoccur_record.tags)
        assert tag_record is not None
    assert reoccur.actions[0].points == reoccur_record.actions[0].points
    assert reoccur.actions[0].action_date == reoccur_record.actions[0].action_date
    assert reoccur.created_date == reoccur_record.created_date
    assert reoccur.modified_date == reoccur_record.modified_date
