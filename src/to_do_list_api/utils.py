import sqlite3
from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends

from to_do_list_api.config import DB_PATH
from to_do_list_api.services import TaskService

SEED_TASKS = [
    ("Buy groceries", False),
    ("Walk the dog", True),
    ("Write the report", False),
]


def get_db() -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    try:
        with conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    done BOOLEAN NOT NULL
                )
                """
            )
            task_count = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
            if not task_count:
                conn.executemany(
                    "INSERT INTO tasks (title, done) VALUES (?, ?)",
                    SEED_TASKS,
                )
        yield conn
    finally:
        conn.close()


DbConn = Annotated[sqlite3.Connection, Depends(get_db)]


def get_task_service(conn: DbConn) -> TaskService:
    return TaskService(conn)


TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]
