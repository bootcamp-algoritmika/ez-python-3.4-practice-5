import json

import falcon

from adapters.interfaces import UserServiceI
from domain.user.dto import UpdateUserDTO, PartiallyUpdateUserDTO, CreateUserDTO
from domain.user.exceptions import UserNotFoundException
from domain.user.schema import UserSchema


class UserResource:
    def __init__(self, service: UserServiceI):
        self.service = service

    def on_get(self, req, resp, user_id):
        try:
            user = self.service.get_user(user_id=user_id)
        except UserNotFoundException as e:
            raise falcon.HTTPNotFound(title=e.message)
        schema = UserSchema()
        resp.body = json.dumps(schema.dump(user))
        resp.status = falcon.HTTP_200

    def on_put(self, req, resp, user_id):
        updated_user = req.media
        dto = UpdateUserDTO(id=user_id, **updated_user)
        try:
            self.service.update_user(user=dto)
        except UserNotFoundException as e:
            raise falcon.HTTPNotFound(title=e.message)
        resp.status = falcon.HTTP_204

    def on_patch(self, req, resp, user_id):
        patched_user = req.media
        dto = PartiallyUpdateUserDTO(id=user_id, **patched_user)
        try:
            self.service.partially_update(user=dto)
        except UserNotFoundException as e:
            raise falcon.HTTPNotFound(title=e.message)
        resp.status = falcon.HTTP_204

    def on_delete(self, req, resp, user_id):
        try:
            self.service.delete_user(user_id=user_id)
        except UserNotFoundException as e:
            raise falcon.HTTPNotFound(title=e.message)
        resp.status = falcon.HTTP_204


class UsersResource:
    def __init__(self, service: UserServiceI):
        self.service = service

    def on_get(self, req, resp):
        limit = req.get_param_as_int('limit') or 50
        offset = req.get_param_as_int('offset') or 0
        order_by = req.get_param('order_by')

        users = self.service.get_users(limit=limit, offset=offset, order_by=order_by)

        schema = UserSchema()
        dict_users = schema.dump(users, many=True)
        resp.body = json.dumps(dict_users)
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        data = req.get_media()
        new_user = CreateUserDTO(**data)
        user_id = self.service.create_user(user=new_user)
        resp.status = falcon.HTTP_201
        resp.location = f'/notes/{user_id}'
