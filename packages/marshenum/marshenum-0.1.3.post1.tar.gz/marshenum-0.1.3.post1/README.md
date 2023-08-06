This library helps to create marshmallow schemas easier.

Derive from RegisteredEnum class to have serializable enum. Set `__load_by_value__` and `__dump_by_value__` to correspondingly load and dump enumerations by their keys or values. Set `__by_value__` for both of them. Default values are `True`.

```
Class Letter(RegisteredEnum):
    __load_by_value__ = False

    a = 'First letter'
    b = 'Second letter'
    ...
```

If request and response schemas have Enum in their fields, you can request a letter and see the value of it, e.g. requesting `a` you will get `First letter`.

Register EnumField to api with
```
api.register_field(EnumField, 'string', None)
```
