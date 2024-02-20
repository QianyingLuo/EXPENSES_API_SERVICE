from typing import Self
from pydantic import Field
from src.application.custom_base_model import CustomBaseModel
from src.domain import expense as domain
from src.domain import common

class CreateExpense(CustomBaseModel):
    name: str

    @classmethod
    def from_domain(cls, expense: domain.CreateExpense ) -> Self:
        return cls.model_validate(expense.model_dump())
    
class GetExpense(CustomBaseModel):
    id: common.ObjectID = Field(alias="_id")
    name: str

    def to_domain(self) -> domain.GetExpense:
        return domain.GetExpense.model_validate(self.model_dump())
    

class UserExpense(CustomBaseModel):
    name: str
    user: common.ObjectID
    quantity: float
    datetime: common.AwareDatetime

    @classmethod
    def from_domain(cls, user_expense: domain.UserExpense ) -> Self:
        return cls.model_validate(user_expense.model_dump())