from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel

def create_task(body:TaskSchema,db : Session ):
    data = body.model_dump()
    new_tasks = TaskModel(title = data["title"],description = data["description"], is_completed = data["is_completed"])

    db.add(new_tasks)
    db.commit()
    db.refresh(new_tasks)
    return { "status": "Task Created Successfully...","data":new_tasks}