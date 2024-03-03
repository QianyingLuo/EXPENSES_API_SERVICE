from typing import Annotated
from fastapi import APIRouter, Body, Depends, Path
from src.controller.request import user_expense_request as request
from src.application import log
from src.domain import common
from src.application.usecases import user_expense_usecases as usecases
from src.application import authorization

logger = log.get_logger(__name__)
router = APIRouter()


@router.post(
    path="/",
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


@router.delete(
    path="/{user_expense_id}",
    response_model=common.DeletionResponse,
    operation_id="Delete User Expense",
    description="Endpoint for deleting user expense",
    dependencies=[Depends(authorization.verify_token)]
)
def delete_user_expense(
    user_expense_id: Annotated[common.ObjectID, Path()]
) -> common.DeletionResponse:
    logger.debug("Expense -> DELETE -> Delete user expense")
    return usecases.delete_user_expense(user_expense_id)