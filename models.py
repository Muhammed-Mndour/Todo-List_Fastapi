from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import validator
from sqlmodel import Field, Session, SQLModel, create_engine, Relationship


class TaskBase(SQLModel):
    title: str
    description: str | None = None
    due_date: datetime | None = None


class CreateTask(TaskBase):
    category_name: str | None = None


class Task(TaskBase, table=True):
    id: int = Field(primary_key=True)
    completed: bool = False
    created_at: datetime = datetime.now()
    category_id: int = Field(default=0, foreign_key="category.id")
    category: Optional["Category"] = Relationship(back_populates="tasks")


class CategoryBase(SQLModel):
    name: str = Field(unique=True)


class CategoryCreate(CategoryBase):

    @validator("name", pre=True)
    def validate_name(cls, value):
        if len(value) < 3:
            raise ValueError("name must be at least 3 characters")
        if not value.isalpha():
            raise ValueError("name must contain only letters")

        return value.title()


class Category(CategoryBase, table=True):
    id: int = Field(primary_key=True)
    tasks: list[Task] = Relationship(back_populates="category")
