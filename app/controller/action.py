import json

from flask import Blueprint, request, jsonify

from app.auth.auth_decorator import authorized
from app.todo.commands.perform_action import PerformAction

action_controller = Blueprint('action', __name__)


@action_controller.route('/action', methods=['POST'])
@authorized
def create():
    action_data = json.loads(request.data)
    todo = PerformAction().execute(action_data)
    return jsonify(todo.to_dict())
