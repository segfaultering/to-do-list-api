from fastapi import APIRouter, HTTPException, status

from to_do_list_api.schemas import TaskCreate, TaskRepr, TaskUpdate
from to_do_list_api.services import TaskNotFoundError
from to_do_list_api.utils import TaskServiceDep

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("")
def list_tasks(service: TaskServiceDep) -> list[TaskRepr]:
    return service.list()


@router.get("/{task_id}")
def read_task(
    task_id: int,
    service: TaskServiceDep,
) -> TaskRepr:
    try:
        return service.get(task_id)
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")


@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    service: TaskServiceDep,
) -> None:
    try:
        service.delete(task_id)
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")


@router.put("/{task_id}")
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    service: TaskServiceDep,
) -> TaskRepr:
    if task_update.title is None and task_update.done is None:
        raise HTTPException(
            status_code=400, detail="At least one of title or done must be provided"
        )
    if task_update.title is not None and not task_update.title.strip():
        raise HTTPException(status_code=400, detail="title must not be empty")
    try:
        return service.update(task_id, task_update)
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")


@router.post("", status_code=status.HTTP_201_CREATED)
def create_task(
    task_create: TaskCreate,
    service: TaskServiceDep,
) -> TaskRepr:
    if not task_create.title.strip():
        raise HTTPException(status_code=400, detail="title must not be empty")
    return service.create(task_create)
