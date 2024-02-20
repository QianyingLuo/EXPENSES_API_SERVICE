from typing import Annotated
from fastapi import APIRouter, Body, Depends, FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import status
from src.controller.request import expense_request as request
from src.application import log
from src.domain import common
from src.application.usecases import expense_usecases as usecases
from src.application import authorization

logger = log.get_logger(__name__)
router = APIRouter()


@router.post(
    path="/",
    response_model=common.CreationResponse,
    operation_id="Create Expense",
    description="Endpoint for creating expense",
    dependencies=[Depends(authorization.verify_token)]
)
def create_expense(
    expense: Annotated[request.CreateExpense, Body()]
) -> common.CreationResponse:
    logger.debug("Expense -> POST -> Create expense")
    return usecases.create_expense(expense.to_domain())


@router.post(
    path="/user",
    response_model=common.CreationResponse,
    operation_id="Create User Expense",
    description="Endpoint for creating user expense",
    dependencies=[Depends(authorization.verify_token)]
)
def add_user_expense(
    expense: Annotated[request.UserExpense, Body()],
) -> common.CreationResponse:
    logger.debug("Expense -> POST -> Create user expense")
    return usecases.add_user_expense(expense.to_domain())


async def expense_already_exists_handler(
    request: Request, exception: common.ExpenseAlreadyExists
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(
            common.GenericHTTPException(
                status_code=str(status.HTTP_400_BAD_REQUEST),
                type="EXPENSE_ALREADY_EXISTS",
                detail=exception.args[0],
            )
        ),
    )

async def expense_not_found_handler(
    request: Request, exception: common.ExpenseNotFound
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(
            common.GenericHTTPException(
                status_code=str(status.HTTP_400_BAD_REQUEST),
                type="EXPENSE_NOT_FOUND",
                detail=exception.args[0],
            )
        ),
    )

def add_expense_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(common.ExpenseNotFound, expense_not_found_handler) # type: ignore
    app.add_exception_handler(common.ExpenseAlreadyExists, expense_already_exists_handler) # type: ignore
