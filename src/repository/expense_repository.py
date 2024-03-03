from typing import Optional

import bson
from src.domain import common
from src.domain import expense as domain
from src.repository.database_connection import database
from src.repository.entity import expense_entity as entity
from pymongo.results import InsertOneResult, DeleteResult

EXPENSE_COLLECTION = "Expense"

def create_expense(expense: domain.CreateExpense) -> common.CreationResponse:
    expense_entity = entity.CreateExpense.from_domain(expense)
    response: InsertOneResult = database.insert_one(
        collection=EXPENSE_COLLECTION, 
        document=expense_entity.model_dump()
    )
    
    return common.CreationResponse(id=response.inserted_id, acknowledged=response.acknowledged)

def delete_expense(expense_id: common.ObjectID) -> common.DeletionResponse:
    response: DeleteResult = database.delete_one(
        collection=EXPENSE_COLLECTION, 
        select={ "_id": bson.ObjectId(expense_id) }
    )
    
    return common.DeletionResponse(deletion_count=response.deleted_count, acknowledged=response.acknowledged)

def get_by_name(name: str) -> Optional[domain.GetExpense]:
    response = database.find_one(
        collection=EXPENSE_COLLECTION,
        select={ "name" : name }
    )
    if not response:
        return None
    
    return entity.GetExpense.model_validate(response).to_domain()

def get_all_expenses() -> list[domain.GetExpense]:
    response = database.find(
        collection=EXPENSE_COLLECTION,
        select={}
    )
    if not response:
        return []
    
    return [entity.GetExpense.model_validate(data).to_domain() for data in response]