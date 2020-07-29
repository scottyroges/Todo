import json

from flask import Blueprint, request, jsonify

from app.auth import get_request
from app.auth.auth_decorator import authorized
from app.todo.commands.add_category import AddCategory
from app.todo.commands.get_categories import GetCategories

category_controller = Blueprint('category', __name__)


@category_controller.route('/category', methods=['POST'])
@authorized
def create():
    category_data = json.loads(request.data)
    if not category_data.get("userId"):
        category_data["userId"] = request.user_id

    category = AddCategory().execute(category_data)
    return jsonify(category.to_dict())


@category_controller.route('/categories', methods=['GET'])
@authorized
def get_categories():
    user_id = request.args.get('userId')
    if user_id is None:
        user_id = get_request().user_id

    categories = GetCategories().execute(user_id)
    return jsonify([category.to_dict() for category in categories])
