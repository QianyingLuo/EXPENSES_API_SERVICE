from typing import Optional
import bson
from pymongo.results import InsertOneResult
from pymongo.command_cursor import CommandCursor
from src.domain.common import CreationResponse

from src.domain.user.user_register import GetUser, PostRegisterUser
from src.repository.database_connection import database
from src.repository.user.domain.get_user_entity import GetUserEntity
from src.repository.user.domain.post_register_user_entity import PostRegisterUserEntity


def post_user(user: PostRegisterUser) -> CreationResponse:
    user_entity = PostRegisterUserEntity.from_domain(user)
    response: InsertOneResult = database.insert(
        collection="User", 
        document=user_entity.model_dump()
    )
    
    return CreationResponse(id=response.inserted_id, acknowledged=response.acknowledged)

def get_user_by_id(id: str) -> Optional[GetUser]:
    pipeline = [{
        "$match": {
            "_id": bson.ObjectId(id)
        }
    }]
    response = database.aggregate(collection="User", pipeline=pipeline)

    if not response:
        return None
    
    user = GetUserEntity.model_validate(response[0])
    return user.to_domain()

def get_user_by_email(email: str) -> Optional[GetUser]:
    pipeline = [{
        "$match": {
            "email": email
        }
    }]
    response = database.aggregate(collection="User", pipeline=pipeline)

    if not response:
        return None
    
    user = GetUserEntity.model_validate(response[0])
    return user.to_domain()