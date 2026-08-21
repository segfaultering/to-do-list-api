import sqlite3

from to_do_list_api.schemas import TaskCreate, TaskRepr, TaskUpdate


class TaskNotFoundError(Exception):
    pass


class TaskService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    done BOOLEAN NOT NULL
                )
                """
            )

    def _fetch_task(self, task_id: int) -> TaskRepr:
        with self.conn:
            row = self.conn.execute(
                "SELECT id, title, done FROM tasks WHERE id = ?",
                (task_id,),
            ).fetchone()
        if row is None:
            raise TaskNotFoundError(f"Task with id {task_id} not found")
        return TaskRepr(id=row[0], title=row[1], done=bool(row[2]))

    def create(self, request: TaskCreate) -> TaskRepr:
        with self.conn:
            cursor = self.conn.execute(
                "INSERT INTO tasks (title, done) VALUES (?, ?)",
                (request.title, False),
            )
            new_id = cursor.lastrowid
        return TaskRepr(id=new_id, title=request.title, done=False)

    def get(self, id: int) -> TaskRepr:
        return self._fetch_task(id)

    def list(self) -> list[TaskRepr]:
        with self.conn:
            rows = self.conn.execute(
                "SELECT id, title, done FROM tasks ORDER BY id"
            ).fetchall()
        return [TaskRepr(id=row[0], title=row[1], done=bool(row[2])) for row in rows]

    def update(self, id: int, request: TaskUpdate) -> TaskRepr:
        existing = self._fetch_task(id)
        new_title = request.title if request.title is not None else existing.title
        new_done = request.done if request.done is not None else existing.done
        with self.conn:
            self.conn.execute(
                "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
                (new_title, new_done, id),
            )
        return TaskRepr(id=id, title=new_title, done=new_done)

    def delete(self, id: int) -> None:
        with self.conn:
            cursor = self.conn.execute("DELETE FROM tasks WHERE id = ?", (id,))
            if cursor.rowcount == 0:
                raise TaskNotFoundError(f"Task with id {id} not found")
