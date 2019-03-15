import json

from flask import Blueprint, request, jsonify

from app.auth.auth_decorator import authorized
from app.todo.commands.add_todo import AddTodo
from app.todo.commands.get_todo import GetTodo
from app.todo.domains.todo_type import TodoType

task_controller = Blueprint('task', __name__)


@task_controller.route('/task', methods=['POST'])
@authorized
def create():
    task_data = json.loads(request.data)

    if not task_data.get("todoOwnerId"):
        task_data["todoOwnerId"] = request.user_id

    task = AddTodo().execute(task_data, TodoType.TASK)
    return jsonify(task.to_dict())


@task_controller.route('/task/<todo_id>', methods=['GET'])
@authorized
def read(todo_id):
    task = GetTodo().execute(todo_id)
    return jsonify(task.to_dict())
