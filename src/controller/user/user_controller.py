from typing import Annotated
from fastapi import APIRouter, Body, Path
from src.application import log
from src.domain.common import CreationResponse, UserAlreadyExists, GenericHTTPException, UserNotFound
from src.controller.user.domain.user_register_response import GetUserResponse, RegisterUser
from src.application.usecases.user import user_creation_usecase, user_get_usecase
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

logger = log.get_logger(__name__)
router = APIRouter()


@router.get(
    path="/{user_id}",
    response_model=GetUserResponse,
    operation_id="Get User",
    description="Endpoint for getting user",
)
def get_user(
    user_id: Annotated[str, Path()]
):
    logger.debug("User -> GET -> Obtain user")
    user = user_get_usecase.get_user(user_id)
    if not user: 
        raise UserNotFound("The user does not exist")
    return GetUserResponse.to_response(user)


@router.post(
    path="/",
    response_model=CreationResponse,
    operation_id="Post User",
    description="Endpoint for creating a new user"
)
def post_user(
    user: Annotated[RegisterUser, Body()]
):
    logger.debug("User -> POST -> Create user")
    return user_creation_usecase.post_user(user.to_domain())


async def user_exists_exception_handler(
    request: Request, exception: UserAlreadyExists
):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=jsonable_encoder(
            GenericHTTPException(
                status_code=str(status.HTTP_409_CONFLICT),
                type="USER_ALREADY_REGISTERED",
                detail=exception.args[0],
            )
        ),
    )

async def user_not_found_exception_handler(
    request: Request, exception: UserNotFound
):
    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT,
        content=jsonable_encoder(
            GenericHTTPException(
                status_code=str(status.HTTP_204_NO_CONTENT),
                type="USER_NOT_FOUND",
                detail=exception.args[0],
            )
        ),
    )


def user_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(UserAlreadyExists, user_exists_exception_handler) # type: ignore
    app.add_exception_handler(UserNotFound, user_not_found_exception_handler) # type: ignore
