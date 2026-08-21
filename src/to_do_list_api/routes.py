from fastapi import APIRouter, HTTPException, status

from to_do_list_api.schemas import TaskRepr, TaskCreate, TaskUpdate

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


@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: int,
) -> None:
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]


@router.put("/{task_id}")
def update_task(
    task_id: int,
    task_update: TaskUpdate,
) -> TaskRepr:
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    if task_update.title is None and task_update.done is None:
        raise HTTPException(status_code=400, detail="At least one of title or done must be provided")
    if task_update.title is not None and not task_update.title.strip():
        raise HTTPException(status_code=400, detail="title must not be empty")
    existing = tasks[task_id]
    new_title = task_update.title if task_update.title is not None else existing.title
    new_done = task_update.done if task_update.done is not None else existing.done
    tasks[task_id] = TaskRepr(id=task_id, title=new_title, done=new_done)
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
