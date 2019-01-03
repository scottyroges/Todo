from app.config import config


def configure_database(app):
    db_uri = config.get("databaseURI")
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    from flask_sqlalchemy import SQLAlchemy
    db = SQLAlchemy(app)
    return db


# def setup_schema(db):
#     for class_ in db.Model._decl_class_registry.values():
#         if hasattr(class_, '__tablename__'):
#             if class_.__name__.endswith('Schema'):
#                 raise ModelConversionError(
#                     "For safety, setup_schema can not be used when a"
#                     "Model class ends with 'Schema'"
#                 )
#
#             class Meta(object):
#                 model = class_
#                 sqla_session = db.session
#
#             schema_class_name = '%sSchema' % class_.__name__
#
#             schema_class = type(
#                 schema_class_name,
#                 (ModelSchema,),
#                 {'Meta': Meta}
#             )
#
#             setattr(class_, '__marshmallow__', schema_class)
