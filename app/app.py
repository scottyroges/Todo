from flask import Flask, jsonify

from app.config import config
from app.controller.action import action_controller
from app.controller.habit import habit_controller
from app.controller.reoccur import reoccur_controller
from app.controller.task import task_controller
from app.database import db
from app.errors import AppError


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = config.get("databaseURI")
    app.config['DEBUG'] = True
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    app.register_blueprint(habit_controller)
    app.register_blueprint(action_controller)
    app.register_blueprint(reoccur_controller)
    app.register_blueprint(task_controller)

    @app.errorhandler(AppError)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
