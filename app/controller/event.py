import json
from flask import jsonify
from flask import request, Blueprint

from app.model.event import Event

event_controller = Blueprint('event', __name__)


@event_controller.route('/event', methods=['POST'])
def create():
    event = _json_to_event(request.data)
    event.save()
    return jsonify(event.to_dict())


def _json_to_event(json_data):
    d = json.loads(json_data)
    event = Event(todo_id=d["todoId"],
                  event_date=d["eventDate"],
                  points=d["points"])
    return event
