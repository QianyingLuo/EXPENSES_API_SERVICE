from typing import Optional
from src.domain import common
from src.domain import expense as domain
from src.repository.database_connection import database
from src.repository.entity import expense_entity as entity
from pymongo.results import InsertOneResult

EXPENSE_COLLECTION = "Expense"

def create_expense(expense: domain.CreateExpense) -> common.CreationResponse:
    expense_entity = entity.CreateExpense.from_domain(expense)
    response: InsertOneResult = database.insert_one(
        collection=EXPENSE_COLLECTION, 
        document=expense_entity.model_dump()
    )
    
    return common.CreationResponse(id=response.inserted_id, acknowledged=response.acknowledged)

def get_by_name(name: str) -> Optional[domain.GetExpense]:
    response = database.find_one(
        collection=EXPENSE_COLLECTION,
        select={ "name" : name }
    )
    if not response:
        return None
    
    return entity.GetExpense.model_validate(response).to_domain()