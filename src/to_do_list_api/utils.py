from collections.abc import Iterator
from typing import Annotated

import psycopg
from fastapi import Depends

from to_do_list_api.config import DATABASE_URL
from to_do_list_api.services import TaskService

SEED_TASKS = [
    ("Buy groceries", False),
    ("Walk the dog", True),
    ("Write the report", False),
]


def get_db() -> Iterator[psycopg.Connection]:
    conn = psycopg.connect(DATABASE_URL)
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    done BOOLEAN NOT NULL
                )
                """
            )
            cur.execute("SELECT COUNT(*) FROM tasks")
            task_count = cur.fetchone()[0]
            if not task_count:
                cur.executemany(
                    "INSERT INTO tasks (title, done) VALUES (%s, %s)",
                    SEED_TASKS,
                )
        conn.commit()
        yield conn
    finally:
        conn.close()


DbConn = Annotated[psycopg.Connection, Depends(get_db)]


def get_task_service(conn: DbConn) -> TaskService:
    return TaskService(conn)


TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]
