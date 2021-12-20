from abc import ABC, abstractmethod

from domain.user.dto import *
from domain.message.dto import *
from domain.user.model import User
from domain.message.model import Message


class UserServiceI(ABC):
    @abstractmethod
    def get_users(self, limit: int, offset: int, order_by: str) -> List[User]: pass

    @abstractmethod
    def get_user(self, user_id) -> User: pass

    @abstractmethod
    def create_user(self, user: CreateUserDTO) -> int: pass

    @abstractmethod
    def delete_user(self, user_id: int) -> None: pass

    @abstractmethod
    def update_user(self, user: UpdateUserDTO) -> None: pass

    @abstractmethod
    def partially_update(self, user: PartiallyUpdateUserDTO) -> None: pass


class MessageServiceI(ABC):
    @abstractmethod
    def get_messages(self, limit: int, offset: int, recent_messages_count: int) -> List[Message]: pass

    @abstractmethod
    def get_message(self, message_id) -> Message: pass

    @abstractmethod
    def create_message(self, message: CreateMessageDTO) -> int: pass

    @abstractmethod
    def delete_message(self, message_id: int) -> None: pass

    @abstractmethod
    def update_message(self, message: UpdateMessageDTO) -> None: pass

    @abstractmethod
    def partially_update(self, message: PartiallyUpdateMessageDTO) -> None: pass
