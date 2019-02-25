from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(session_options=dict(expire_on_commit=False,
                                     autoflush=False,
                                     weak_identity_map=False))
