import json

from flask import Blueprint, request, jsonify

from app.auth.auth_decorator import authorized
from app.todo.commands.add_category import AddCategory

category_controller = Blueprint('category', __name__)


@category_controller.route('/category', methods=['POST'])
@authorized
def create():
    category_data = json.loads(request.data)
    if not category_data.get("userId"):
        category_data["userId"] = request.user_id

    category = AddCategory().execute(category_data)
    return jsonify(category.to_dict())
