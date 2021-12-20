import json

import falcon

from adapters.interfaces import MessageServiceI
from domain.message.dto import UpdateMessageDTO, PartiallyUpdateMessageDTO, CreateMessageDTO
from domain.message.exceptions import MessageNotFoundException
from domain.message.schema import MessageSchema
from domain.user.exceptions import UserNotFoundException


class MessageResource:
    def __init__(self, service: MessageServiceI):
        self.service = service

    def on_get(self, req, resp, message_id):
        try:
            message = self.service.get_message(message_id=message_id)
        except MessageNotFoundException as e:
            raise falcon.HTTPNotFound(title=e.message)
        schema = MessageSchema()
        resp.body = json.dumps(schema.dump(message))
        resp.status = falcon.HTTP_200

    def on_put(self, req, resp, message_id):
        updated_message = req.media
        dto = UpdateMessageDTO(id=message_id, **updated_message)
        try:
            self.service.update_message(message=dto)
        except MessageNotFoundException as e:
            raise falcon.HTTPNotFound(title=e.message)
        except UserNotFoundException as e:
            raise falcon.HTTPNotFound(title=e.message)
        resp.status = falcon.HTTP_204

    def on_patch(self, req, resp, message_id):
        patched_message = req.media
        dto = PartiallyUpdateMessageDTO(id=message_id, **patched_message)
        try:
            self.service.partially_update(message=dto)
        except MessageNotFoundException as e:
            raise falcon.HTTPNotFound(title=e.message)
        except UserNotFoundException as e:
            raise falcon.HTTPNotFound(title=e.message)
        resp.status = falcon.HTTP_204

    def on_delete(self, req, resp, message_id):
        try:
            self.service.delete_message(message_id=message_id)
        except MessageNotFoundException as e:
            raise falcon.HTTPNotFound(title=e.message)
        resp.status = falcon.HTTP_204


class MessagesResource:
    def __init__(self, service: MessageServiceI):
        self.service = service

    def on_get(self, req, resp):
        recent_messages_count = req.get_param_as_int('recent_messages')
        limit = req.get_param_as_int('limit') or 50
        offset = req.get_param_as_int('offset') or 0

        messages = self.service.get_messages(limit=limit, offset=offset, recent_messages_count=recent_messages_count)

        schema = MessageSchema()
        dict_messages = schema.dump(messages, many=True)
        resp.body = json.dumps(dict_messages)
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        data = req.get_media()
        new_message = CreateMessageDTO(**data)
        try:
            message_id = self.service.create_message(message=new_message)
        except UserNotFoundException as e:
            raise falcon.HTTPNotFound(title=e.message)
        resp.status = falcon.HTTP_201
        resp.location = f'/notes/{message_id}'
