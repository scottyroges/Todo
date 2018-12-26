def load_models():
    from .habit import Habit
    from .event import Event
    from .category import Category
    from .tag import Tag


def load_schemas(db):
    from marshmallow_sqlalchemy import ModelConversionError, ModelSchema
    from app.utils.helper_methods import to_camel_case

    for class_ in db.Model._decl_class_registry.values():
        if hasattr(class_, '__tablename__'):
            if class_.__name__.endswith('Schema'):
                raise ModelConversionError(
                    "For safety, setup_schema can not be used when a"
                    "Model class ends with 'Schema'"
                )

            class Meta(object):
                model = class_
                sqla_session = db.session

            schema_class_name = '%sSchema' % class_.__name__
            props = {'Meta': Meta}
            if hasattr(class_, '__schema_fields__'):
                props.update(class_.__schema_fields__)

            schema_class = type(
                schema_class_name,
                (ModelSchema,),
                props
            )
            underscore_fields = (x for x in schema_class._declared_fields
                                 if "_" in x)
            for field in underscore_fields:
                name = to_camel_case(field)
                schema_class._declared_fields[field].dump_to = name
                schema_class._declared_fields[field].load_from = name

            setattr(class_, '__marshmallow__', schema_class)
