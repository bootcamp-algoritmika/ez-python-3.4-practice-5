from sqlalchemy import func
from sqlalchemy.orm import subqueryload

from domain.user.model import User
from domain.message.model import Message
from domain.user.exceptions import UserNotFoundException
from domain.user.storage import UserStorageI
from domain.user.dto import CreateUserDTO, PartiallyUpdateUserDTO, UpdateUserDTO
from adapters.db.db_init import Session


class UserStorage(UserStorageI):

    def create(self, user: CreateUserDTO) -> int:
        with Session() as session:
            new_user = User(
                name=user.name,
                nickname=user.nickname
            )
            session.add(new_user)
            session.commit()
            new_user_id = new_user.id
        return new_user_id

    def update(self, user: UpdateUserDTO) -> None:
        with Session() as session:
            user_query: User = session.query(User).filter(User.id == user.id).one_or_none()
            if not user_query:
                raise UserNotFoundException(message="user not found")
            user_query.name = user.name
            user_query.nickname = user.nickname
            session.flush()
            session.commit()

    def partial_update(self, user: PartiallyUpdateUserDTO) -> None:
        with Session() as session:
            user_query: User = session.query(User).filter(User.id == user.id).one_or_none()
            if not user_query:
                raise UserNotFoundException(message="user not found")
            if user.name is not None:
                user_query.name = user.name
            if user.nickname is not None:
                user_query.nickname = user.nickname
            session.flush()
            session.commit()

    def delete(self, user_id: int) -> None:
        with Session() as session:
            user_query = session.query(User).filter(User.id == user_id).one_or_none()
            if not user_query:
                raise UserNotFoundException(message="user not found")
            session.delete(user_query)
            session.commit()

    def get_one(self, user_id: str) -> User:
        with Session() as session:
            user_query = session.query(User).options(
                subqueryload(User.messages)
            ).filter(User.id == user_id).one_or_none()
            if not user_query:
                raise UserNotFoundException(message="user not found")
        return user_query

    def get_all(self, limit: int, offset: int, order_by: str) -> list[User]:
        with Session() as session:
            query = session.query(User)
            query_with_order_by = self.ordering_query(query=query, order_by=order_by)
            users = query_with_order_by.options(
                subqueryload(User.messages)
            ).offset(offset).limit(limit).all()
            return users

    def ordering_query(self, query, order_by):
        if order_by == 'name':
            query = query.order_by(User.name)
        elif order_by == 'message_time':
            query.join(Message).order_by(Message.created_at)
        return query
