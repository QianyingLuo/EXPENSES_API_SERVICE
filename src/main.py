from fastapi import FastAPI
from .routes import example
import uvicorn

app = FastAPI()
app.include_router(example.router, prefix="/example")
