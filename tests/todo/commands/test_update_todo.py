import datetime

import pytest
from dateutil.tz import tzutc

from app.errors import UnauthorizedError
from app.todo.commands.update_todo import UpdateTodo
from app.todo.domains.todo_type import TodoType
from app.todo.transformers.task_transformer import TaskTransformer
from app.utils import make


class TestUpdateTodo:
    def test_update_todo(self, user_request, todo_repo):
        task = todo_repo.add(
            TaskTransformer.from_record(
                make.a_task(session=None,
                            todo_owner_id=user_request.get("user_id"))
            )
        )

        new_category = make.a_category(session=None, name="new category", color="#aa1133")

        todo_data = {
            "name": "updated task",
            "todoId": task.todo_id,
            "todoOwnerId": "123",
            "description": "description",
            "todoType": "TASK",
            "completionPoints": 3,
            "dueDate": "2019-05-02 22:48:05",
            "category": {
                "id": new_category.id
            },
            "tags": ["who", "knows"]
        }

        updated_todo = UpdateTodo().execute(todo_data)

        assert updated_todo is not None
        assert updated_todo.todo_id == task.todo_id
        assert updated_todo.todo_owner.owner_id == user_request.get("user_id")
        assert updated_todo.name == todo_data["name"]
        assert updated_todo.todo_type == TodoType.TASK
        assert updated_todo.completion_points == todo_data["completionPoints"]
        assert updated_todo.due_date == datetime.datetime(2019, 5, 2, 22, 48, 5, tzinfo=tzutc())
        assert updated_todo.category.category_id == new_category.id

    def test_update_todo_unauthorized(self, user_request, todo_repo):
        task = todo_repo.add(
            TaskTransformer.from_record(
                make.a_task(session=None,
                            todo_owner_id="456")
            )
        )

        new_category = make.a_category(session=None, name="new category", color="#aa1133")

        todo_data = {
            "name": "updated task",
            "todoId": task.todo_id,
            "todoOwnerId": "456",
            "description": "description",
            "todoType": "TASK",
            "completionPoints": 3,
            "dueDate": "2019-05-02 22:48:05",
            "category": {
                "id": new_category.id
            },
            "tags": ["who", "knows"]
        }

        with pytest.raises(UnauthorizedError):
            UpdateTodo().execute(todo_data)
