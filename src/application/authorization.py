from typing import Annotated
from fastapi import HTTPException, Header
import jwt

async def verify_token(authorization: Annotated[str, Header()]):
    if not authorization:
        raise HTTPException(status_code=400, detail="Bearer token not provided")
    
    authorization = authorization.replace("Bearer ", "")

    jwt.decode(
        authorization,
        "token_secret",
        algorithms=["HS256"],
        options={"verify_signature": True},
    )
    
async def user_info(authorization: Annotated[str, Header()]):
    if not authorization:
        raise HTTPException(status_code=400, detail="Bearer token not provided")
    
    authorization = authorization.replace("Bearer ", "")

    return jwt.decode(
        authorization,
        "token_secret",
        algorithms=["HS256"],
        options={"verify_signature": True},
    )