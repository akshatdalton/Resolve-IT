from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Question:
    title: str
    description: str
    tags: Optional[List[str]]
    votes: int


@dataclass
class Answer:
    description: str
    votes: int
