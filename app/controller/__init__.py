

def register_controllers(app):
    from app.controller.habit import habit_controller
    app.register_blueprint(habit_controller)

    from app.controller.event import event_controller
    app.register_blueprint(event_controller)
