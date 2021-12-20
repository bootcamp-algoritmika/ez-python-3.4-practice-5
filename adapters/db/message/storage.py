from sqlalchemy.orm import subqueryload

from domain.message.exceptions import MessageNotFoundException
from domain.user.model import User
from domain.user.exceptions import UserNotFoundException
from domain.message.model import Message
from domain.message.storage import MessageStorageI
from domain.message.dto import CreateMessageDTO, PartiallyUpdateMessageDTO, UpdateMessageDTO
from adapters.db.db_init import Session


class MessageStorage(MessageStorageI):

    def create(self, message: CreateMessageDTO) -> int:
        with Session() as session:
            author: User = session.query(User).filter(User.id == message.author).one_or_none()
            if not author:
                raise UserNotFoundException(message="user not found")
            new_message = Message(
                text=message.text
            )
            new_message.author = author
            session.add(new_message)
            session.flush()
            new_message_id = new_message.id
            session.commit()
        return new_message_id

    def update(self, message: UpdateMessageDTO) -> None:
        with Session() as session:
            message_query: Message = session.query(Message).filter(Message.id == message.id).one_or_none()
            if not message_query:
                raise MessageNotFoundException(message="message not found")
            author: User = session.query(User).filter(User.id == message.author).one_or_none()
            if not author:
                raise UserNotFoundException(message="user not found")
            message_query.text = message.text
            message_query.author = author
            session.flush()
            session.commit()

    def partial_update(self, message: PartiallyUpdateMessageDTO) -> None:
        with Session() as session:
            message_query: Message = session.query(Message).filter(Message.id == message.id).one_or_none()
            if not message_query:
                raise MessageNotFoundException(message="message not found")
            if message.author is not None:
                author: User = session.query(User).filter(User.id == message.author).one_or_none()
                if not author:
                    raise UserNotFoundException(message="user not found")
                message_query.author = author
            if message.text is not None:
                message_query.text = message.text
            session.flush()
            session.commit()

    def delete(self, message_id: int) -> None:
        with Session() as session:
            message_query: Message = session.query(Message).filter(Message.id == message_id).one_or_none()
            if not message_query:
                raise MessageNotFoundException(message="message not found")
            session.delete(message_query)
            session.commit()

    def get_one(self, message_id: str) -> Message:
        with Session() as session:
            message_query: Message = session.query(Message).options(
                subqueryload(Message.author)
            ).filter(Message.id == message_id).one_or_none()
            if not message_query:
                raise MessageNotFoundException(message="message not found")
        return message_query

    def get_all(self, limit: int, offset: int, recent_messages_count: int) -> list[Message]:
        with Session() as session:
            if not recent_messages_count:
                return session.query(Message).options(subqueryload(Message.author)).offset(offset).limit(limit).all()
            messages = session.query(Message).options(
                subqueryload(Message.author)
            ).order_by(Message.created_at).limit(recent_messages_count).all()
            return messages
