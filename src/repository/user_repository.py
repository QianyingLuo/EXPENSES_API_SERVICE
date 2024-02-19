from typing import Optional
import bson
from pymongo.results import InsertOneResult, UpdateResult
from pymongo.command_cursor import CommandCursor
from src.domain.common import CreationResponse

from src.domain.user import GetUser, RegisterUser
from src.repository.database_connection import database
from src.repository.entity.user_entity import GetUserEntity, RegisterUserEntity

USER_COLLECTION = "User"

def post_user(user: RegisterUser) -> CreationResponse:
    user_entity = RegisterUserEntity.from_domain(user)
    response: InsertOneResult = database.insert_one(
        collection="User", 
        document=user_entity.model_dump()
    )
    
    return CreationResponse(id=response.inserted_id, acknowledged=response.acknowledged)


def get_user_by_email(email: str) -> Optional[GetUser]:
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
    
    user = GetUserEntity.model_validate(response[0])
    return user.to_domain()

def update_token(id: str, token: str):
    response: UpdateResult = database.update_one(
        collection=USER_COLLECTION,
        select={ "_id": bson.ObjectId(id) },
        update={ "$set": { "token": token } }    
    )

    return response.acknowledged