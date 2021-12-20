from marshmallow import Schema
from marshmallow.fields import String, Integer, Nested

from ..message.schema import MessageUserSchema


class UserSchema(Schema):
    id = Integer()
    name = String()
    nickname = String()
    messages = Nested(MessageUserSchema(), many=True)
