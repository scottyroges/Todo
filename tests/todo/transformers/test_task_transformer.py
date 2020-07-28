import datetime

from freezegun import freeze_time
from app.model import (
    Task as TaskRecord,
    Category as CategoryRecord,
    Tag as TagRecord,
    Action as ActionRecord
)
from app.todo.domains.todo_owner import TodoOwner
from app.todo.domains.category import Category as DomainCategory
from app.todo.domains.tag import Tag as DomainTag
from app.todo.domains.action import Action as DomainAction
from app.todo.domains.task.task import Task as DomainTask
from app.todo.domains.todo_type import TodoType
from app.todo.transformers.task_transformer import TaskTransformer


@freeze_time("2019-02-24")
def test_to_record():
    todo_owner = TodoOwner(owner_id="123")
    tags = [DomainTag(name="who"), DomainTag(name="knows")]
    actions = [DomainAction()]
    task = DomainTask(todo_id="abc",
                      todo_owner=todo_owner,
                      name="task",
                      description="description",
                      completion_points=1,
                      due_date=datetime.datetime(2019, 3, 2, 11, 34, 5),
                      category=DomainCategory(category_id="abc",
                                              name="test",
                                              color="#FFF"),
                      tags=tags,
                      actions=actions)

    task_record = TaskTransformer.to_record(task)

    assert task_record.todo_id == task.todo_id
    assert task_record.todo_owner_id == task.todo_owner.owner_id
    assert task_record.name == task.name
    assert task_record.description == task.description
    assert task_record.completion_points == task.completion_points
    assert task_record.due_date == task.due_date

    assert task_record.category.id == "abc"
    assert task_record.category.name == "test"
    assert task_record.category.color == "#FFF"

    for tag_record in task_record.tags:
        tag = filter(lambda x: x.name == tag_record.name, task.tags)
        assert tag is not None
    assert task_record.actions[0].points == task.actions[0].points
    assert task_record.actions[0].action_date == task.actions[0].action_date
    assert task_record.created_date == task.created_date
    assert task_record.modified_date == task.modified_date


def test_from_record():
    tags = [TagRecord(name="who"), TagRecord(name="knows")]
    actions = [ActionRecord(action_date=datetime.datetime(2019, 2, 24),
                            points=1)]
    task_record = TaskRecord(todo_id="abc",
                             todo_owner_id="123",
                             name="task",
                             description="description",
                             todo_type=TodoType.TASK,
                             completion_points=1,
                             due_date=datetime.datetime(2019, 3, 2, 21, 37, 5),
                             category=CategoryRecord(id="abc",
                                                     name="test",
                                                     color="#FFF"),
                             tags=tags,
                             actions=actions,
                             created_date=datetime.datetime(2019, 2, 24),
                             modified_date=datetime.datetime(2019, 2, 24))

    task = TaskTransformer.from_record(task_record)

    assert task.todo_id == task_record.todo_id
    assert task.todo_owner.owner_id == task_record.todo_owner_id
    assert task.name == task_record.name
    assert task.description == task_record.description
    assert task.completion_points == task_record.completion_points
    assert task.due_date == task_record.due_date
    assert task.category.category_id == "abc"
    assert task.category.name == "test"
    assert task.category.color == "#FFF"
    for tag in task.tags:
        tag_record = filter(lambda x: x.name == tag.name, task_record.tags)
        assert tag_record is not None
    assert task.actions[0].points == task_record.actions[0].points
    assert task.actions[0].action_date == task_record.actions[0].action_date
    assert task.created_date == task_record.created_date
    assert task.modified_date == task_record.modified_date
