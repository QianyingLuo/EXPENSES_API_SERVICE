from src.application.custom_base_model import CustomBaseModel
from src.domain import expense as domain

class CreateExpense(CustomBaseModel):
    name: str

    def to_domain(self) -> domain.CreateExpense:
        return domain.CreateExpense.model_validate(self.model_dump())
    

