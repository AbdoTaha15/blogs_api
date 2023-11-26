from sqlmodel import Field, Column, SQLModel
from sqlalchemy.dialects.sqlite import TEXT
from typing import Optional


class Blog(SQLModel, table=True):
    __tablename__ = "Blog"

    id: Optional[int] = Field(primary_key=True, default=None)
    title: str = Field(max_length=255, nullable=False)
    body: str = Field(sa_column=Column(TEXT))
    author: str = Field(max_length=255, nullable=False)
