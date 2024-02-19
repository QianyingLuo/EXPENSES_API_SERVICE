from typing import Annotated
from fastapi import APIRouter, Body, Depends, Path
from src.domain.user import JwtUser
from src.application import log
from src.domain.common import CreationResponse, InvalidCredentials, UserAlreadyExists, GenericHTTPException, UserNotFound
from src.controller.request.user_request import RegisterUserRequest, LoginCredentialsRequest
from src.controller.response.user_response import GetUserResponse, LoginResultResponse, LogoutResultResponse
from src.application.usecases import user_usecases
from src.application import authorization
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

logger = log.get_logger(__name__)
router = APIRouter()


@router.get(
    path="/auth/{user_id}",
    response_model=GetUserResponse,
    operation_id="Get User",
    description="Endpoint for getting user",
)
def get_user(
    user_id: Annotated[str, Path()]
) -> GetUserResponse:
    logger.debug("User -> GET -> Obtain user")
    user = user_usecases.get_user(user_id)
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
    user: Annotated[RegisterUserRequest, Body()]
) -> CreationResponse:
    logger.debug("User -> POST -> Create user")
    return user_usecases.post_user(user.to_domain())


@router.post(
    path="/login",
    response_model=LoginResultResponse,
    operation_id="Login User",
    description="Endpoint for evaluate login",
)
def login_user(
    credentials: Annotated[LoginCredentialsRequest, Body()],
) -> LoginResultResponse:
    logger.debug("User -> POST -> Login user")
    login_result = user_usecases.login(credentials.to_domain())
    return LoginResultResponse.to_response(login_result)


@router.get(
    path="/logout",
    response_model=LogoutResultResponse,
    operation_id="Logout User",
    description="Endpoint for evaluate logout",
    dependencies=[Depends(authorization.verify_token)]
)
def logout_user(
    user_info: Annotated[dict, Depends(authorization.user_info)]
) -> LogoutResultResponse:
    logger.debug("User -> GET -> Logout user")
    user_usecases.logout(JwtUser.model_validate(user_info))
    return LogoutResultResponse(result=str(status.HTTP_200_OK))



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


async def invalid_credentials_exception_handler(
    request: Request, exception: InvalidCredentials
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(
            GenericHTTPException(
                status_code=str(status.HTTP_400_BAD_REQUEST),
                type="INVALID_CREDENTIALS",
                detail=exception.args[0],
            )
        ),
    )

def user_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(UserAlreadyExists, user_exists_exception_handler) # type: ignore
    app.add_exception_handler(UserNotFound, user_not_found_exception_handler) # type: ignore
    app.add_exception_handler(InvalidCredentials, invalid_credentials_exception_handler) # type: ignore

