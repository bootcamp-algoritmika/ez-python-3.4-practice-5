from abc import ABC, abstractmethod

from .model import Message
from .dto import UpdateMessageDTO, PartiallyUpdateMessageDTO, CreateMessageDTO


class MessageStorageI(ABC):

    @abstractmethod
    def get_one(self, message_id: int) -> Message:
        pass

    @abstractmethod
    def get_all(self, limit: int, offset: int, recent_messages_count: int) -> list[Message]:
        pass

    @abstractmethod
    def create(self, message: CreateMessageDTO) -> int:
        pass

    @abstractmethod
    def update(self, message: UpdateMessageDTO) -> None:
        pass

    @abstractmethod
    def partial_update(self, message: PartiallyUpdateMessageDTO) -> None:
        pass

    @abstractmethod
    def delete(self, message_id: int) -> None:
        pass
