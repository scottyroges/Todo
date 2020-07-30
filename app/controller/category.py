import json

from flask import Blueprint, request, jsonify

from app.auth import get_request
from app.auth.auth_decorator import authorized
from app.auth.auth_util import is_admin
from app.errors import UnauthorizedError
from app.todo.commands.add_category import AddCategory
from app.todo.commands.get_categories import GetCategories
from app.todo.commands.update_category import UpdateCategory

category_controller = Blueprint('category', __name__)


@category_controller.route('/category', methods=['POST'])
@authorized
def create():
    category_data = json.loads(request.data)
    if not category_data.get("userId"):
        category_data["userId"] = request.user_id

    category = AddCategory().execute(category_data)
    return jsonify(category.to_dict())


@category_controller.route('/category', methods=['PUT'])
@authorized
def update():
    category_data = json.loads(request.data)

    category = UpdateCategory().execute(category_data)
    return jsonify(category.to_dict())


@category_controller.route('/categories', methods=['GET'])
@category_controller.route('/categories/<user_id>', methods=['GET'])
@authorized
def get_categories(user_id=None):
    request_user_id = get_request().user_id
    if user_id is not None and request_user_id != user_id and not is_admin():
        raise UnauthorizedError()

    if user_id is None:
        user_id = request_user_id

    categories = GetCategories().execute(user_id)
    return jsonify([category.to_dict() for category in categories])
