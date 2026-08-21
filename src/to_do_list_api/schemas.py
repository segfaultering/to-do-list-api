from pydantic import BaseModel


class TaskRepr(BaseModel):
    id: int
    title: str
    done: bool


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None
