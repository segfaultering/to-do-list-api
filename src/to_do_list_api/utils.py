from to_do_list_api.schemas import TaskRepr


def get_tasks() -> dict[int, TaskRepr]:
    return {
        1: TaskRepr(id=1, title="Buy groceries", done=False),
        2: TaskRepr(id=2, title="Walk the dog", done=True),
        3: TaskRepr(id=3, title="Write the report", done=False),
        4: TaskRepr(id=4, title="Clean the house", done=True),
    }
