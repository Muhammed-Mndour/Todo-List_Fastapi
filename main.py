from datetime import datetime, date
from enum import Enum
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager

from sqlmodel import Session, select

from models import Task, Category, CreateTask, CategoryCreate, UpdateTask
from db import get_session

app = FastAPI()


def get_or_create_category(session: Session, category_name: str) -> Category:
    category = session.exec(select(Category).where(Category.name == category_name.title())).first()
    if not category:
        category = Category(name=category_name.title())
        session.add(category)
        session.commit()
        session.refresh(category)
    return category


@app.get("/", tags=["Hello"])
def read_root():
    return {"hello": datetime.now().time()}


@app.post("/tasks", tags=["Tasks"])
def create_task(
        task_data: CreateTask,
        session: Session = Depends(get_session)
) -> Task:

    # Create the task
    task = Task()
    task_data = task_data.dict(exclude_unset=True)
    for key, value in task_data.items():
        if key == "category_name":
            category = get_or_create_category(session, task_data["category_name"])
            task.category_id = category.id
        else:
            setattr(task, key, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.get("/tasks", tags=["Tasks"])
def get_all_tasks(
        session: Session = Depends(get_session),
        completed: bool | None = None,
        category_name: str | None = None,
        due_date_from: date | None = date(1900, 1, 1),
        due_date_to: date | None = date(3000, 1, 1)
) -> list[Task]:
    tasks = session.exec(select(Task)).all()
    if completed:
        tasks = [task for task in tasks if task.completed == completed]

    if category_name:
        category = session.exec(select(Category).where(Category.name == category_name.title())).first()
        tasks = [task for task in tasks if category and task.category_id == category.id]

    if due_date_from:
        tasks = [task for task in tasks if task.due_date and task.due_date.date() >= due_date_from]

    if due_date_to:
        tasks = [task for task in tasks if task.due_date and task.due_date.date() <= due_date_to]

    return tasks


@app.get("/tasks/{task_id}", tags=["Tasks"])
def get_single_task(
        task_id,
        session: Session = Depends(get_session)
) -> Task:
    task = session.exec(select(Task).where(Task.id == task_id)).first()
    if task:
        return task

    raise HTTPException(status_code=404, detail="Task not found")


@app.put("/tasks/{task_id}", tags=["Tasks"])
def update_task(
        task_id: int,
        task_data: UpdateTask,
        session: Session = Depends(get_session)
) -> Task:
    task = session.exec(select(Task).where(Task.id == task_id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task_data = task_data.dict(exclude_unset=True)
    if task_data:
        for key, value in task_data.items():
            if key == "category_name":
                value = get_or_create_category(session, value).id
                task.category_id = value
            else:
                setattr(task, key, value)
    session.commit()
    session.refresh(task)
    return task


@app.delete("/tasks/{task_id}", tags=["Tasks"])
def delete_task(
        task_id: int,
        session: Session = Depends(get_session)
):
    task = session.exec(select(Task).where(Task.id == task_id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task does not exist")
    session.delete(task)
    session.commit()
    return {"message": "Task deleted successfully", "task_id": task_id}


@app.post("/categories", tags=["Categories"])
def create_category(
        category_data: CategoryCreate,
        session: Session = Depends(get_session)
) -> Category:
    category = get_or_create_category(session, category_data.name)
    return category


@app.get("/categories", tags=["Categories"])
def get_categories(session: Session = Depends(get_session)) -> list[Category]:
    categories = session.exec(select(Category)).all()
    return categories


@app.delete("/categories/{category_id}", tags=["Categories"])
def delete_category(category_id: int, session: Session = Depends(get_session)):
    category = session.exec(select(Category).where(Category.id == category_id)).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    associated_tasks = session.exec(select(Task).where(Task.category_id == category_id)).first()
    if associated_tasks:
        raise HTTPException(status_code=409, detail="Cannot delete category with associated tasks")

    session.delete(category)
    session.commit()
    return {"message": "Category deleted successfully", "category_id": category_id}


category_names = [
    "Work", "Personal", "Shopping", "Health", "Education",
    "Travel", "Hobbies", "Fitness", "Finance", "Technology"
]

# Sample task data with title, description, and category_id
task_data = [
    ("Finish report", "Complete the project report", datetime(2025, 2, 3, 0, 0, 0), 1),  # Category ID 1
    ("Buy groceries", "Get vegetables and fruits", datetime(2025, 2, 4, 0, 0, 0), 2),  # Category ID 2
    ("Attend meeting", "Participate in the project update meeting", datetime(2025, 2, 5, 0, 0, 0), 3),  # Category ID 3
    ("Call client", "Follow up with the client regarding the proposal", datetime(2025, 2, 6, 0, 0, 0), 4),
    # Category ID 4
    ("Schedule appointment", "Book a doctor's appointment", datetime(2025, 2, 7, 0, 0, 0), 5),  # Category ID 5
    ("Write email", "Send the weekly progress email", datetime(2025, 2, 8, 0, 0, 0), 6),  # Category ID 6
    ("Clean house", "Tidy up the living room and kitchen", datetime(2025, 2, 9, 0, 0, 0), 7),  # Category ID 7
    ("Prepare presentation", "Create slides for the upcoming presentation", datetime(2025, 2, 10, 0, 0, 0), 8),
    # Category ID 8
    ("Workout", "Do a 30-minute workout", datetime(2025, 2, 11, 0, 0, 0), 9),  # Category ID 9
    ("Read book", "Finish the first chapter of the book", datetime(2025, 2, 12, 0, 0, 0), 10),  # Category ID 10
]


@app.get("/create_metadata", tags=["create_metadata"])
def create_metadata(session: Session = Depends(get_session)):
    for category_name in category_names:
        category = Category(name=category_name)
        session.add(category)
    session.commit()  # Commit to save the categories

    # Insert Tasks with category_id linked
    for task_title, task_description, due_date, category_id in task_data:
        task = Task(title=task_title, description=task_description,
                    due_date=due_date, category_id=category_id)
        session.add(task)
    session.commit()  # Commit to save the tasks
