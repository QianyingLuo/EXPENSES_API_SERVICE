from fastapi import FastAPI

from .routes import example

app = FastAPI()
app.include_router(example.router, prefix="/example")
