from pydantic import BaseModel


class TaskRepr(BaseModel):
    id: int
    title: str
    done: bool


class TaskCreate(BaseModel):
    title: str
