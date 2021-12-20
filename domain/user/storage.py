from abc import ABC, abstractmethod

from domain.user.model import User
from domain.user.dto import UpdateUserDTO, PartiallyUpdateUserDTO, CreateUserDTO


class UserStorageI(ABC):

    @abstractmethod
    def get_one(self, user_id: int) -> User:
        pass

    @abstractmethod
    def get_all(self, limit: int, offset: int, order_by: str) -> list[User]:
        pass

    @abstractmethod
    def create(self, user: CreateUserDTO) -> int:
        pass

    @abstractmethod
    def update(self, user: UpdateUserDTO) -> None:
        pass

    @abstractmethod
    def partial_update(self, user: PartiallyUpdateUserDTO) -> None:
        pass

    @abstractmethod
    def delete(self, user_id: int) -> None:
        pass
