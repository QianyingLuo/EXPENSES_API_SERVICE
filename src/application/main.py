from fastapi import FastAPI
from src.application.environment import read_jwt_environment

from src.controller import user_controller
from src.controller import expense_controller
from src.controller.user_controller import user_exception_handlers
from src.controller.expense_controller import expense_exception_handlers

app = FastAPI()

def start_application() -> None:
    
    read_jwt_environment()
    user_exception_handlers(app)
    expense_exception_handlers(app)
    
    # Configure router
    app.include_router(user_controller.router, prefix="/user")
    app.include_router(expense_controller.router, prefix="/expense")

start_application()