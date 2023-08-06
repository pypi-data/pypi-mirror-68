import attr
import marshmallow as ma
from marshmallow.exceptions import ValidationError
from marshmallow_annotations.ext.attrs import AttrsSchema


def attr_with_schema(**kwargs):
    def decorator(cls):
        schema_meta = getattr(cls, 'SchemaMeta', object)
        fields = attr.fields(cls)

        class Schema(AttrsSchema):
            class Meta(schema_meta):
                locals().update(kwargs)
                target = cls

        for field in fields:
            if field.default == attr.NOTHING:
                Schema._declared_fields[field.name].required = True

        cls.schema = Schema
        Schema.__name__ = cls.__name__ + "Schema"

        def attr_iter(self):
            return iter(self.__dict__.items())

        cls.__iter__ = attr_iter
        return cls
    return decorator
