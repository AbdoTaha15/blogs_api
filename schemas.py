from sqlmodel import SQLModel
from typing import Optional


class BlogSchema(SQLModel):
    title: Optional[str]
    body: Optional[str]
    author: Optional[str]
