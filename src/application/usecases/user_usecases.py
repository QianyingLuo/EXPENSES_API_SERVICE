from typing import Optional
from fastapi import HTTPException, status
import jwt
import bcrypt
from src.domain.user import GetUser, JwtUser, LoginCredentials, LoginResult
from src.repository import user_repository
from src.domain.common import CreationResponse, InvalidCredentials, UserAlreadyExists, UserNotFound
from src.domain.user import RegisterUser
from src.repository import user_repository
from src.application.environment import jwt_environment_variables


def get_user(id: str) -> Optional[GetUser]:
    return user_repository.get_user_by_id(id)


def post_user(user: RegisterUser) -> CreationResponse:

    if user_repository.get_user_by_email(user.email):
        raise UserAlreadyExists("It seems that this account is already registered")

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), salt)
    user.password = hashed_password.decode('utf-8')
    return user_repository.post_user(user)

def login(credentials: LoginCredentials) -> LoginResult:
    user = user_repository.get_user_by_email(credentials.email)

    if not user:
        raise InvalidCredentials("The credentials provided are not valid")
    
    password_is_valid = bcrypt.checkpw(
        credentials.password.encode('utf-8'), 
        user.password.encode('utf-8')
    )
    
    if not password_is_valid:
        raise InvalidCredentials("The credentials provided are not valid")

    user_jwt = JwtUser.model_validate(user.model_dump())
    secret_jwt = jwt_environment_variables["TOKEN_SECRET"]
    encoded_jwt = jwt.encode(user_jwt.model_dump(), secret_jwt, algorithm="HS256")

    user.token = encoded_jwt
    result = user_repository.update_token(user.id, encoded_jwt)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Some error occured. Contact with devs.toni@gmail.com"
        )
    
    return LoginResult(
        firstname=user_jwt.firstname,
        lastname=user_jwt.lastname,
        email=user_jwt.email,
        token=encoded_jwt
    )
    
