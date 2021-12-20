from typing import List

from adapters.interfaces import MessageServiceI
from .dto import CreateMessageDTO, UpdateMessageDTO, PartiallyUpdateMessageDTO
from .model import Message
from .storage import MessageStorageI


class MessageService(MessageServiceI):
    def __init__(self, storage: MessageStorageI):
        self.storage = storage

    def get_messages(self, limit: int, offset: int, recent_messages_count: int) -> List[Message]:
        return self.storage.get_all(limit=limit, offset=offset, recent_messages_count=recent_messages_count)

    def get_message(self, message_id: int) -> Message:
        return self.storage.get_one(message_id=message_id)

    def create_message(self, message: CreateMessageDTO) -> int:
        return self.storage.create(message=message)

    def delete_message(self, message_id: int) -> None:
        return self.storage.delete(message_id=message_id)

    def update_message(self, message: UpdateMessageDTO) -> None:
        return self.storage.update(message=message)

    def partially_update(self, message: PartiallyUpdateMessageDTO) -> None:
        return self.storage.partial_update(message=message)
