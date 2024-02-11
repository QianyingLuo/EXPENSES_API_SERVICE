from src.domain.common import CreationResponse, UserAlreadyExists
from src.domain.user.user_register import PostRegisterUser
from src.repository.user import user_repository

def post_user(user: PostRegisterUser) -> CreationResponse:
    if not user_repository.get_user_by_email(user.email):
        return user_repository.post_user(user)
    
    raise UserAlreadyExists("It seems that this account is already registered")