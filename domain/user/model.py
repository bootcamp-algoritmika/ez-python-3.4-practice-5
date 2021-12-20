from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Table

from ..message.model import Message
from ..mapper import mapper_registry, metadata


@dataclass
class User:
    id: int = field(init=False)
    name: str = None
    nickname: str = None
    messages: list[Message] = field(default_factory=list)
    
    
user_table = Table(
    'user', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String),
    Column('nickname', String)
)
mapper_registry.map_imperatively(
    User, user_table,
    properties={
        'messages': relationship(Message, lazy='subquery', backref='author')
    }
)
