from app.config import config


def configure_database(app):
    db_uri = config.get("databaseURI")
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_ECHO"] = True
    from flask_sqlalchemy import SQLAlchemy
    db = SQLAlchemy(app, session_options=dict(expire_on_commit=False,
                                              autoflush=False,
                                              weak_identity_map=False))
    return db


def load_models():
    # hiding this a little bit
    from app import model
