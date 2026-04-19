from fastapi import FastAPI
from src.utils.db import Base,engine
from src.tasks.models import TaskModel

Base.metadata.create_all(engine)

app = FastAPI(title = "This is my task management app.")