from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root() -> dict[str, str | list[str]]:
    return {
        "name": "Task API",
        "version": "0.1.0",
        "endpoints": ["/", "/health", "/tasks"],
    }


@app.get("/health")
def read_health() -> dict[str, str]:
    return {"status": "ok"}
