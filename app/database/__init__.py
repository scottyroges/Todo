from app.config import config
from app.todo.adpaters.sqlalchemy.data_mappers.habit_data_mapper import HabitDataMapper


def configure_database(app):
    db_uri = config.get("databaseURI")
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    from flask_sqlalchemy import SQLAlchemy
    db = SQLAlchemy(app, session_options=dict(expire_on_commit=False))

    HabitDataMapper.configure_mappings(db)
    return db
