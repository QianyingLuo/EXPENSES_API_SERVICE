from src.domain import common
from src.domain import expense as domain
from src.repository import expense_repository
from src.repository import user_expense_repository
from src.repository import user_repository


def add_user_expense(user_expense: domain.UserExpense) -> common.CreationResponse:
    valid_user = user_repository.get_user_by_id(user_expense.user)
    valid_expense = expense_repository.get_by_name(user_expense.name)

    if not valid_user:
        raise common.UserNotFound("The user you're trying to assign a expense doesn't exist")
    
    if not valid_expense:
        raise common.ExpenseNotFound("The expense you're trying to save doesn't exist")
    
    expense_exists = user_expense_repository.already_exists(user_expense)

    if expense_exists:
        raise common.ExpenseAlreadyExists("This expense is already registered")
    
    return user_expense_repository.add_user_expense(user_expense)


def delete_user_expense(user_expense_id: common.ObjectID) -> common.DeletionResponse:
    return user_expense_repository.delete_user_expense(user_expense_id)