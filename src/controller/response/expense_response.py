from datetime import date
from typing import Self
from pydantic import EmailStr, Field
from pydantic_extra_types.phone_numbers import PhoneNumber
from src.application.custom_base_model import CustomBaseModel
from src.domain import expense as domain


class GetExpense(CustomBaseModel):
    id: str
    name: str

    @classmethod
    def to_response(cls, expense: domain.GetExpense) -> Self:
        return cls.model_validate(expense.model_dump())
    

