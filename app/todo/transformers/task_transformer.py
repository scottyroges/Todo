from app.model import (
    Action as ActionRecord,
    Category as CategoryRecord,
    Task as TaskRecord,
    Tag as TagRecord
)
from app.todo.domains.action import Action as DomainAction
from app.todo.domains.task.task import Task as DomainTask
from app.todo.domains.category import Category as DomainCategory
from app.todo.domains.reoccur.reoccur_repeat import ReoccurRepeat, ReoccurRepeatType
from app.todo.domains.tag import Tag as DomainTag
from app.todo.domains.todo_owner import TodoOwner


class TaskTransformer:
    @classmethod
    def to_record(cls, task: DomainTask):
        categories = [CategoryRecord(id=category.category_id,
                                     name=category.name)
                      for category in task.categories]

        tags = [TagRecord(id=tag.tag_id,
                          name=tag.name)
                for tag in task.tags]

        actions = [ActionRecord(id=action.action_id,
                                action_date=action.action_date,
                                points=action.points)
                   for action in task.actions]

        return TaskRecord(todo_id=task.todo_id,
                          todo_owner_id=task.todo_owner.owner_id,
                          name=task.name,
                          description=task.description,
                          todo_type=task.todo_type,
                          completion_points=task.completion_points,
                          due_date=task.due_date,
                          categories=categories,
                          tags=tags,
                          actions=actions,
                          created_date=task.created_date,
                          modified_date=task.modified_date)

    @classmethod
    def from_record(cls, task_record: TaskRecord):
        todo_owner = TodoOwner(owner_id=task_record.todo_owner_id)
        categories = [DomainCategory(category_id=category.id,
                                     name=category.name)
                      for category in task_record.categories]
        tags = [DomainTag(tag_id=tag.id,
                          name=tag.name)
                for tag in task_record.tags]

        actions = [DomainAction(action_id=action.id,
                                action_date=action.action_date,
                                points=action.points)
                   for action in task_record.actions]
        return DomainTask(todo_id=task_record.todo_id,
                          todo_owner=todo_owner,
                          name=task_record.name,
                          description=task_record.description,
                          completion_points=task_record.completion_points,
                          due_date=task_record.due_date,
                          categories=categories,
                          tags=tags,
                          actions=actions,
                          created_date=task_record.created_date,
                          modified_date=task_record.modified_date)
