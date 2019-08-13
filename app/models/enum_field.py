from marshmallow_enum import EnumField as BaseEnumField


# todo: revert it once https://github.com/justanr/marshmallow_enum/issues/23 is resolved
class EnumField(BaseEnumField):
    def _deserialize(self, value, attr, data, **kwargs):
        return super(EnumField, self)._deserialize(value, attr, data)
