# To-Do List API

A simple CRUD API for a to-do list application built with FastAPI.

## What it does

This API provides endpoints to manage a to-do list:
- List all tasks
- Get a single task by ID
- Create a new task
- Update an existing task
- Delete a task

## Database

This API stores tasks in a **SQLite** database (`data/tasks.db`). The previous version used a simple in-memory dictionary, which meant all data was lost every time the server restarted. Switching to SQLite solves this by persisting tasks to disk.

**What is SQLite?** SQLite is a lightweight, self-contained relational database engine. Unlike traditional database servers (PostgreSQL, MySQL), it runs entirely within your application process and stores the entire database in a single file. It requires no separate server process, no configuration, and no external dependencies.

**Why SQLite over an in-memory store?**

- **Persistence** -- Data survives server restarts and process crashes.
- **Querying** -- SQL gives you powerful filtering, ordering, and aggregation capabilities that are tedious to implement manually with dictionaries.
- **Concurrency safety** -- SQLite handles concurrent access with built-in locking, avoiding race conditions.
- **Portability** -- The entire database is a single file that can be copied, backed up, or inspected with tools like [SQLiteBrowser](https://sqlitebrowser.org/).

## Setup & Running

### Prerequisites

- Python 3.12+
- `uv` package manager

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd to-do-list-api

# Install dependencies
uv sync
```

### Running the server

```bash
./run.sh
```

The server will start at `http://localhost:8000`.

### Examples

#### cURL output

![cURL output](media/curl_output.PNG)

#### OpenAPI/SwaggerUI docs

![OpenAPI docs](media/openapi_docs.PNG)

#### SQLite database (via SQLiteBrowser)

![SQLiteBrowser](media/sqlitebrowser.PNG)

## API Endpoints

| Method | Endpoint         | Description                      | Response |
|--------|------------------|----------------------------------|----------|
| GET    | `/`              | Root endpoint, lists available routes | JSON     |
| GET    | `/health`        | Health check                     | `{"status": "ok"}` |
| GET    | `/tasks`         | List all tasks                   | `list[TaskRepr]` |
| GET    | `/tasks/{task_id}` | Get a single task by ID        | `TaskRepr` |
| POST   | `/tasks`         | Create a new task                | `TaskRepr` |
| DELETE | `/tasks/{task_id}` | Delete a task by ID             | **204 No Content** |
| PUT    | `/tasks/{task_id}` | Update a task by ID             | `TaskRepr` |

### Request/Response models

**TaskRepr:**
- `id` (int) - Unique identifier
- `title` (str) - Task title
- `done` (bool) - Whether the task is completed

**TaskCreate:**
- `title` (str, required) - Task title. Must not be empty.

**TaskUpdate:**
- `title` (str, optional) - New title. Must not be empty if provided.
- `done` (bool, optional) - New completion status. Mutually exclusive with title in the sense that at least one must be provided.

### Error responses

- **400** - Bad request (e.g., empty title, both fields None in update)
- **404** - Task not found
- **422** - Validation error (FastAPI default, e.g., missing required fields)
