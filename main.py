from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager

from sqlmodel import Session, select

from models import Task, Category, CreateTask, CategoryCreate
from db import get_session

app = FastAPI()


@app.get("/")
def read_root():
    return {"hello": datetime.now().time()}


@app.post("/task")
async def create_task(
        task_data: CreateTask,
        session: Session = Depends(get_session)
) -> Task:
    category = session.exec(select(Category).where(Category.name == task_data.category_name.title())).first()
    if not category:
        category = Category(name=task_data.category_name)
        session.add(category)
        session.commit()
        session.refresh(category)

    # Create the task
    task = Task(
        title=task_data.title,
        description=task_data.description,
        due_date=task_data.due_date,
        category_id=category.id
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.post("/category")
async def create_category(
        category_data: CategoryCreate,
        session: Session = Depends(get_session)
) -> Category:
    category = Category(**category_data.dict())
    session.add(category)
    session.commit()
    session.refresh(category)
    return category






category_names = [
    "Work", "Personal", "Shopping", "Health", "Education",
    "Travel", "Hobbies", "Fitness", "Finance", "Technology"
]

# Sample task data with title, description, and category_id
task_data = [
    ("Finish report", "Complete the project report", 1),  # Category ID 1
    ("Buy groceries", "Get vegetables and fruits", 2),  # Category ID 2
    ("Attend meeting", "Participate in the project update meeting", 3),  # Category ID 3
    ("Call client", "Follow up with the client regarding the proposal", 4),  # Category ID 4
    ("Schedule appointment", "Book a doctor's appointment", 5),  # Category ID 5
    ("Write email", "Send the weekly progress email", 6),  # Category ID 6
    ("Clean house", "Tidy up the living room and kitchen", 7),  # Category ID 7
    ("Prepare presentation", "Create slides for the upcoming presentation", 8),  # Category ID 8
    ("Workout", "Do a 30-minute workout", 9),  # Category ID 9
    ("Read book", "Finish the first chapter of the book", 10),  # Category ID 10
]


@app.get("/create_metadata")
def create_metadata(session: Session = Depends(get_session)):
    for category_name in category_names:
        category = Category(name=category_name)
        session.add(category)
    session.commit()  # Commit to save the categories

    # Insert Tasks with category_id linked
    for task_title, task_description, category_id in task_data:
        task = Task(title=task_title, description=task_description, category_id=category_id)
        session.add(task)
    session.commit()  # Commit to save the tasks
