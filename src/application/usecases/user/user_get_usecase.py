from typing import Optional
from src.domain.user.user_register import GetUser
from src.repository.user import user_repository


def get_user(id: str) -> Optional[GetUser]:
    return user_repository.get_user_by_id(id)