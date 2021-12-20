from typing import List

from adapters.interfaces import UserServiceI
from domain.user.dto import CreateUserDTO, UpdateUserDTO, PartiallyUpdateUserDTO
from domain.user.model import User
from domain.user.storage import UserStorageI


class UserService(UserServiceI):
    def __init__(self, storage: UserStorageI):
        self.storage = storage

    def get_users(self, limit: int, offset: int, order_by: str) -> List[User]:
        return self.storage.get_all(limit=limit, offset=offset, order_by=order_by)

    def get_user(self, user_id: int) -> User:
        return self.storage.get_one(user_id=user_id)

    def create_user(self, user: CreateUserDTO) -> int:
        return self.storage.create(user=user)

    def delete_user(self, user_id) -> None:
        return self.storage.delete(user_id=user_id)

    def update_user(self, user: UpdateUserDTO) -> None:
        return self.storage.update(user=user)

    def partially_update(self, user: PartiallyUpdateUserDTO) -> None:
        return self.storage.partial_update(user=user)
