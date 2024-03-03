from typing import Annotated
from fastapi import APIRouter, Body, Depends, FastAPI, Path, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import status
from src.controller.request import expense_request as request
from src.application import log
from src.domain import common
from src.application.usecases import expense_usecases as usecases
from src.application import authorization
from src.controller.response import expense_response as response

logger = log.get_logger(__name__)
router = APIRouter()

@router.get(
    path="/",
    response_model=list[response.GetExpense],
    operation_id="Get Expenses",
    description="Endpoint for getting all expenses",
    dependencies=[Depends(authorization.verify_token)]
)
def get_all_expenses() -> list[response.GetExpense]:
    logger.debug("Expense -> GET -> Get expenses")
    expenses = usecases.get_all_expenses()
    return [response.GetExpense.to_response(expense) for expense in expenses]

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

@router.delete(
    path="/{expense_id}",
    response_model=common.DeletionResponse,
    operation_id="Delete Expense",
    description="Endpoint for deleting expense",
    dependencies=[Depends(authorization.verify_token)]
)
def delete_expense(
    expense_id: Annotated[common.ObjectID, Path()]
) -> common.DeletionResponse:
    logger.debug("Expense -> DELETE -> Delete expense")
    return usecases.delete_expense(expense_id)


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
