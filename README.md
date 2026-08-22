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

This API stores tasks in a **PostgreSQL** database. The database runs as a Docker container (image: `postgres:16-trixie`) and is managed via the `run.sh` script, which handles container creation and startup automatically.

The connection string is loaded from a `.env` file at the project root using `python-dotenv`. See `.env.example` for the expected variables:

```
POSTGRES_PASSWORD=password
POSTGRES_DB=tasks
DATABASE_URL=postgresql://postgres:password@localhost:5432/tasks
```

**Why PostgreSQL over SQLite?**

- **Concurrency** -- PostgreSQL handles many simultaneous connections efficiently with MVCC, while SQLite serializes writes.
- **Advanced features** -- Full support for JSON columns, full-text search, window functions, CTEs, and more.
- **Scalability** -- Can be scaled to handle large datasets and high throughput workloads.
- **Production standard** -- Battle-tested in production systems worldwide with robust replication and backup tooling.

## Setup & Running

### Prerequisites

- Python 3.12+
- `uv` package manager
- Docker (for the PostgreSQL container)

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd to-do-list-api

# Install dependencies
uv sync

# Set up environment variables
cp .env.example .env
# Edit .env with your preferred credentials
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
