from src.domain import common
from src.domain import expense as domain
from src.repository import expense_repository

def create_expense(expense: domain.CreateExpense) -> common.CreationResponse:
    expense_saved = expense_repository.get_by_name(expense.name)

    if expense_saved:
        raise common.ExpenseAlreadyExists("This expense is already registered")
    
    return expense_repository.create_expense(expense)

def delete_expense(expense_id: common.ObjectID) -> common.DeletionResponse: 
    return expense_repository.delete_expense(expense_id)

def get_all_expenses() -> list[domain.GetExpense]:
    return expense_repository.get_all_expenses()