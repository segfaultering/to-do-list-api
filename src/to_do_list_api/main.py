from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root() -> str:
    return "Hello World!"
