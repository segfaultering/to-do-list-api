import psycopg

from to_do_list_api.schemas import TaskCreate, TaskRepr, TaskUpdate


class TaskNotFoundError(Exception):
    pass


class TaskService:
    def __init__(self, conn: psycopg.Connection) -> None:
        self.conn = conn

    def _fetch_task(self, task_id: int) -> TaskRepr:
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT id, title, done FROM tasks WHERE id = %s",
                (task_id,),
            )
            row = cur.fetchone()
        if row is None:
            raise TaskNotFoundError(f"Task with id {task_id} not found")
        return TaskRepr(id=row[0], title=row[1], done=row[2])

    def create(self, request: TaskCreate) -> TaskRepr:
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id",
                (request.title, False),
            )
            new_id = cur.fetchone()[0]
        self.conn.commit()
        return TaskRepr(id=new_id, title=request.title, done=False)

    def get(self, id: int) -> TaskRepr:
        return self._fetch_task(id)

    def list(self) -> list[TaskRepr]:
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, title, done FROM tasks ORDER BY id")
            rows = cur.fetchall()
        return [TaskRepr(id=row[0], title=row[1], done=row[2]) for row in rows]

    def update(self, id: int, request: TaskUpdate) -> TaskRepr:
        existing = self._fetch_task(id)
        new_title = request.title if request.title is not None else existing.title
        new_done = request.done if request.done is not None else existing.done
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE tasks SET title = %s, done = %s WHERE id = %s",
                (new_title, new_done, id),
            )
        self.conn.commit()
        return TaskRepr(id=id, title=new_title, done=new_done)

    def delete(self, id: int) -> None:
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM tasks WHERE id = %s", (id,))
            if cur.rowcount == 0:
                raise TaskNotFoundError(f"Task with id {id} not found")
        self.conn.commit()
