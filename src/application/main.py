from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.application.environment import read_jwt_environment

from src.controller import user_controller, expense_controller, user_expense_controller
from src.controller.user_controller import add_user_exception_handlers
from src.controller.expense_controller import add_expense_exception_handlers

app = FastAPI()

def start_application() -> None:
    
    # Read environment
    read_jwt_environment()

    # Add exception handlers
    add_user_exception_handlers(app)
    add_expense_exception_handlers(app)

    origins = [
        "http://10.0.2.2",
        "http://localhost"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Configure router
    app.include_router(user_controller.router, prefix="/user")
    app.include_router(expense_controller.router, prefix="/expense")
    app.include_router(user_expense_controller.router, prefix="/user-expense")

start_application()