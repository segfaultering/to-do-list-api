from pydantic import BaseModel


class TaskRepr(BaseModel):
    id: int
    title: str
    done: bool
