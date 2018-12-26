from marshmallow import fields


class SmartNested(fields.Nested):

    def serialize(self, attr, obj, accessor=None):
        if attr not in obj.__dict__:
            return {'id': int(getattr(obj, attr))}
        return super(SmartNested, self).serialize(attr, obj, accessor)