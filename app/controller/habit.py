import json
from flask import jsonify
from flask import request, Blueprint

from app.auth.auth_decorator import authorized
from app.todo.commands.add_todo import AddTodo
from app.todo.commands.get_todo import GetTodo
from app.todo.domains.todo_type import TodoType

habit_controller = Blueprint('habit', __name__)


@habit_controller.route('/habit', methods=['POST'])
@authorized
def create():
    habit_data = json.loads(request.data)

    if not habit_data.get("todoOwnerId"):
        habit_data["todoOwnerId"] = request.user_id

    habit = AddTodo().execute(habit_data, TodoType.HABIT)
    return jsonify(habit.to_dict())


@habit_controller.route('/habit/<todo_id>', methods=['GET'])
@authorized
def read(todo_id):
    habit = GetTodo().execute(todo_id)
    return jsonify(habit.to_dict())
