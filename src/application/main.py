from fastapi import FastAPI

from src.controller.user import user_controller
from src.controller.user.user_controller import user_exception_handlers

app = FastAPI()

def start_application() -> None:
    
    user_exception_handlers(app)
    
    # Configure router
    app.include_router(user_controller.router, prefix="/user")

start_application()