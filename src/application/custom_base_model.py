from typing import Any
import bson
import pydantic

class CustomBaseModel(pydantic.BaseModel):

    @pydantic.model_validator(mode="before")
    @classmethod
    def parse_mongo(cls, data: Any) -> Any:
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, bson.ObjectId):
                    data[k] = str(v)
        return data