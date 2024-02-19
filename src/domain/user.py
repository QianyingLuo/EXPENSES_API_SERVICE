from datetime import date, timedelta
from typing import Optional
from pydantic_extra_types.phone_numbers import PhoneNumber
from pydantic import EmailStr
from src.application.custom_base_model import CustomBaseModel


class RegisterUser(CustomBaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    birthday: date
    phone_number: PhoneNumber
    password: str
    token: Optional[str] = None

class GetUser(CustomBaseModel):
    id: str
    name: str
    firstname: str
    lastname: str
    email: EmailStr
    birthday: date
    phone_number: PhoneNumber
    password: str
    token: Optional[str] = None

class JwtUser(CustomBaseModel):
    firstname: str
    lastname: str
    email: EmailStr

class LoginCredentials(CustomBaseModel):
    email: EmailStr
    password: str

class LoginResult(CustomBaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    token: str