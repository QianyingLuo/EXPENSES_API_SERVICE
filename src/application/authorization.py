from typing import Annotated
from fastapi import Depends, HTTPException, Header

async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    
async def auth_exists(authorization: Annotated[str, Header()]):
    if authorization:
        raise ValueError()