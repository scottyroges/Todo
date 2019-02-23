

def register_controllers(app):
    from app.controller.habit import habit_controller
    app.register_blueprint(habit_controller)

    from app.controller.action import action_controller
    app.register_blueprint(action_controller)
