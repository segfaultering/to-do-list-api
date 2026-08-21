import sqlite3
from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends

from to_do_list_api.config import DB_PATH
from to_do_list_api.services import TaskService


def get_db() -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    try:
        yield conn
    finally:
        conn.close()


DbConn = Annotated[sqlite3.Connection, Depends(get_db)]


def get_task_service(conn: DbConn) -> TaskService:
    return TaskService(conn)


TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]
