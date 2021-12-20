from dataclasses import dataclass


@dataclass
class CreateMessageDTO:
    text: str
    author: int


@dataclass
class UpdateMessageDTO:
    id: int
    text: str
    author: int


@dataclass
class PartiallyUpdateMessageDTO:
    id: int
    text: str = None
    author: int = None
