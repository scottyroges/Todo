import json
import logging

from flask import Blueprint, jsonify, request

from app.auth import get_request
from app.auth.auth_decorator import authorized
from app.auth.auth_util import is_admin
from app.errors import UnauthorizedError
from app.todo.commands.add_todo import AddTodo
from app.todo.commands.get_todo import GetTodo
from app.todo.commands.get_todos import GetAllTodos

todo_controller = Blueprint('todo', __name__)

logger = logging.getLogger(__name__)


@todo_controller.route('/todo/<todo_id>', methods=['GET'])
@authorized
def read(todo_id):
    todo = GetTodo().execute(todo_id)
    return jsonify(todo.to_dict())


@todo_controller.route('/todo', methods=['POST'])
@authorized
def create():
    todo_data = json.loads(request.data)

    if not todo_data.get("todoOwnerId"):
        todo_data["todoOwnerId"] = request.user_id

    todo = AddTodo().execute(todo_data)
    return jsonify(todo.to_dict())


@todo_controller.route('/todos', methods=['GET'])
@todo_controller.route('/todos/<user_id>', methods=['GET'])
@authorized
def read_all(user_id=None):
    request_user_id = get_request().user_id
    if user_id is not None and request_user_id != user_id and not is_admin():
        raise UnauthorizedError()

    if user_id is None:
        user_id = request_user_id

    todos = GetAllTodos().execute(user_id)
    return jsonify([todo.to_dict() for todo in todos])

