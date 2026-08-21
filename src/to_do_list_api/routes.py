from typing import Annotated

from fastapi import APIRouter, HTTPException, status

from to_do_list_api.schemas import TaskRepr, TaskCreate

router = APIRouter(prefix="/tasks", tags=["tasks"])

tasks: dict[int, TaskRepr] = {
    1: TaskRepr(id=1, title="Buy groceries", done=False),
    2: TaskRepr(id=2, title="Walk the dog", done=True),
    3: TaskRepr(id=3, title="Write the report", done=False),
    4: TaskRepr(id=4, title="Clean the house", done=True),
}


@router.get("")
def list_tasks() -> list[TaskRepr]:
    return list(tasks.values())


@router.get("/{task_id}")
def read_task(
    task_id: int,
) -> TaskRepr:
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]


@router.post("", status_code=status.HTTP_201_CREATED)
def create_task(
    task_create: TaskCreate,
) -> TaskRepr:
    if not task_create.title.strip():
        raise HTTPException(status_code=400, detail="title must not be empty")
    new_id = max(tasks.keys()) + 1 if tasks else 1
    new_task = TaskRepr(id=new_id, title=task_create.title, done=False)
    tasks[new_id] = new_task
    return new_task
