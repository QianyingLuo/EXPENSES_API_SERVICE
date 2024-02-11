from fastapi import FastAPI
from src.application.environment import read_jwt_environment

from src.controller import user_controller
from src.controller.user_controller import user_exception_handlers

app = FastAPI()

def start_application() -> None:
    
    read_jwt_environment()
    user_exception_handlers(app)
    
    # Configure router
    app.include_router(user_controller.router, prefix="/user")

start_application()