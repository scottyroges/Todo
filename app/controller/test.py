from flask import Blueprint

test_controller = Blueprint('test', __name__)


@test_controller.route('/test/hello', methods=['GET'])
def hello():
    return "hello"




