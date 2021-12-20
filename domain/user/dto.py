from dataclasses import dataclass
from typing import List


@dataclass
class CreateUserDTO:
    name: str
    nickname: str


@dataclass
class UpdateUserDTO:
    id: int
    name: str
    nickname: str


@dataclass
class PartiallyUpdateUserDTO:
    id: int
    name: str = None
    nickname: str = None
