import bson
from src.domain import common
from src.domain import expense as domain
from src.repository.database_connection import database
from src.repository.entity import expense_entity as entity
from pymongo.results import InsertOneResult, DeleteResult

USER_EXPENSE_COLLECTION = "UserExpense"


def already_exists(user_expense: domain.UserExpense) -> bool:
    user_expense_entity = entity.UserExpense.from_domain(user_expense)
    response = database.find_one(
        collection=USER_EXPENSE_COLLECTION,
        select={ 
            "name" : user_expense_entity.name,
            "datetime": user_expense_entity.datetime,
            "quantity": user_expense_entity.quantity,
            "user": user_expense_entity.user
        }
    )
    if not response:
        return False
    
    return True


def add_user_expense(user_expense: domain.UserExpense) -> common.CreationResponse:
    user_expense_entity = entity.UserExpense.from_domain(user_expense)

    
    response: InsertOneResult = database.insert_one(
        collection=USER_EXPENSE_COLLECTION,
        document=user_expense_entity.model_dump()
    )
    
    return common.CreationResponse(id=response.inserted_id, acknowledged=response.acknowledged)


def delete_user_expense(user_expense_id: common.ObjectID) -> common.DeletionResponse:
    response: DeleteResult = database.delete_one(
        collection=USER_EXPENSE_COLLECTION,
        select={ "_id": bson.ObjectId(user_expense_id) }
    )
    
    return common.DeletionResponse(deletion_count=response.deleted_count, acknowledged=response.acknowledged)