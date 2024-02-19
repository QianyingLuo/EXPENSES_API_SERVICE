from typing import Optional
import bson
from pymongo.results import InsertOneResult, UpdateResult
from src.domain import common

from src.domain import user as domain
from src.repository.database_connection import database
from src.repository.entity import user_entity as entity

USER_COLLECTION = "User"

def post_user(user: domain.RegisterUser) -> common.CreationResponse:
    user_entity = entity.RegisterUserEntity.from_domain(user)
    response: InsertOneResult = database.insert_one(
        collection=USER_COLLECTION, 
        document=user_entity.model_dump()
    )
    
    return common.CreationResponse(id=response.inserted_id, acknowledged=response.acknowledged)


def get_user_by_email(email: str) -> Optional[domain.GetUser]:
    pipeline = [{
        "$match": {
            "email": email
        }
    }]
    response = database.aggregate(
        collection=USER_COLLECTION, 
        pipeline=pipeline
    )

    if not response:
        return None
    
    user = entity.GetUserEntity.model_validate(response[0])
    return user.to_domain()

def update_token(id: str, token: str):
    response: UpdateResult = database.update_one(
        collection=USER_COLLECTION,
        select={ "_id": bson.ObjectId(id) },
        update={ "$set": { "token": token } }    
    )

    return response.acknowledged