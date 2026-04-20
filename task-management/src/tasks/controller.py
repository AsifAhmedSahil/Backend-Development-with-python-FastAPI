from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel
from src.user.models import UserModel
from fastapi import HTTPException

def create_task(body:TaskSchema,db : Session,user:UserModel ):
    data = body.model_dump()
    new_tasks = TaskModel(title = data["title"],description = data["description"], is_completed = data["is_completed"], user_id = user.id)

    db.add(new_tasks)
    db.commit()
    db.refresh(new_tasks)
    return new_tasks

def get_tasks(db:Session):
    tasks = db.query(TaskModel).all()
    return tasks


def get_one_task(task_id:int,db:Session):

    one_task = db.query(TaskModel).get(task_id)
    if not one_task:
        raise HTTPException(404, detail="Task id not found in database")

    return one_task

def update_task(body:TaskSchema,task_id:int,db:Session):
    one_task = db.query(TaskModel).get(task_id)
    if not one_task:
        raise HTTPException(404, detail="Task id not found in database")
    
    body = body.model_dump()

    for field,value in body.items():
        setattr(one_task,field,value)


    

    db.add(one_task)
    db.commit()
    db.refresh(one_task)

    return one_task


def delete_task(task_id:int,db:Session):
    one_task = db.query(TaskModel).get(task_id)
    if not one_task:
        raise HTTPException(404,detail="Task id not found!")

    db.delete(one_task)
    db.commit()

    return None