from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from to_do_list_api.schemas import TaskRepr
from to_do_list_api.utils import get_tasks

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("")
def list_tasks(
    tasks: Annotated[dict[int, TaskRepr], Depends(get_tasks)],
) -> list[TaskRepr]:
    return list(tasks.values())


@router.get("/{task_id}")
def read_task(
    task_id: int,
    tasks: Annotated[dict[int, TaskRepr], Depends(get_tasks)],
) -> TaskRepr:
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]
