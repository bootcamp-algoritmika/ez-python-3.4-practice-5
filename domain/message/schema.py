from marshmallow import Schema, pre_dump
from marshmallow.fields import String, Integer, DateTime


class MessageSchema(Schema):
    id = Integer()
    text = String()
    author = Integer()
    created_at = DateTime()
    updated_at = DateTime()

    @pre_dump
    def message_predump(self, data, **kwargs):
        result = {
            'author': data.author.id,
            'text': data.text,
            'created_at': data.created_at,
            'updated_at': data.updated_at
        }
        return result


class MessageUserSchema(Schema):
    id = Integer()
    text = String()
    created_at = DateTime()
    updated_at = DateTime()
