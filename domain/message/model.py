from dataclasses import field, dataclass
from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, Text, TIMESTAMP, func, Table, String

from ..mapper import mapper_registry, metadata

from typing import TYPE_CHECKING, Any



@dataclass
class Message:
    id: int = field(init=False)
    text: str = None
    author: Any = None
    created_at: datetime = None
    updated_at: datetime = None


message_table = Table(
    'message', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String),
    Column('text', Text),
    Column('created_at', TIMESTAMP, server_default=func.now()),
    Column("author_id", Integer, ForeignKey('user.id')),
    Column('updated_at', TIMESTAMP, server_default=func.now(), onupdate=func.now())
)
mapper_registry.map_imperatively(
    Message, message_table
)
