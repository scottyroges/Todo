import json
from flask import jsonify
from flask import request, Blueprint

from app.auth.auth_decorator import authorized
from app.auth.auth_util import is_owner_or_admin
from app.errors import MarshallingError, UnauthorizedError, NotFoundError
from app.model.habit import Habit

habit_controller = Blueprint('habit', __name__)


@habit_controller.route('/habit', methods=['POST'])
@authorized
def create():
    # TODO: maybe turn this into a decorator
    habit, error = Habit.__marshmallow__().load(json.loads(request.data))
    if error:
        raise MarshallingError(error)

    if habit.user_id:
        if not is_owner_or_admin(habit.user_id):
            raise UnauthorizedError("authorized user does not have permission "
                                    "to create habit for specified user")
    else:
        habit.user_id = request.user_id

    habit.save()
    return jsonify(Habit.__marshmallow__().dump(habit).data)


@habit_controller.route('/habit/<id>', methods=['GET'])
@authorized
def read(id):
    habit = Habit.query.filter_by(id=id).first()

    if not habit:
        raise NotFoundError("No habit with id %s" % id)

    if not is_owner_or_admin(habit.user_id):
        raise UnauthorizedError("authorized user does not have permission "
                                "to habit")

    return jsonify(Habit.__marshmallow__().dump(habit).data)
