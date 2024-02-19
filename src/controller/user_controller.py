from typing import Annotated
from fastapi import APIRouter, Body, Depends
from src.domain import user as domain
from src.application import log
from src.domain import common
from src.controller.request import user_request as request
from src.controller.response import user_response as response
from src.application.usecases import user_usecases as usecases
from src.application import authorization
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

logger = log.get_logger(__name__)
router = APIRouter()


@router.get(
    path="/auth/info",
    response_model=response.GetUserResponse,
    operation_id="Get User",
    description="Endpoint for getting user",
)
def get_user(
    user_info: Annotated[dict, Depends(authorization.user_info)]
) -> response.GetUserResponse:
    logger.debug("User -> GET -> Obtain user")
    user = usecases.get_user(domain.JwtUser.model_validate(user_info))
    if not user: 
        raise common.UserNotFound("The user does not exist")
    return response.GetUserResponse.to_response(user)


@router.post(
    path="/",
    response_model= common.CreationResponse,
    operation_id="Post User",
    description="Endpoint for creating a new user"
)
def post_user(
    user: Annotated[request.RegisterUserRequest, Body()]
) -> common.CreationResponse:
    logger.debug("User -> POST -> Create user")
    return usecases.post_user(user.to_domain())


@router.post(
    path="/login",
    response_model=response.LoginResultResponse,
    operation_id="Login User",
    description="Endpoint for evaluate login",
)
def login_user(
    credentials: Annotated[request.LoginCredentialsRequest, Body()],
) -> response.LoginResultResponse:
    logger.debug("User -> POST -> Login user")
    login_result = usecases.login(credentials.to_domain())
    return response.LoginResultResponse.to_response(login_result)


@router.get(
    path="/logout",
    response_model=response.LogoutResultResponse,
    operation_id="Logout User",
    description="Endpoint for evaluate logout",
    dependencies=[Depends(authorization.verify_token)]
)
def logout_user(
    user_info: Annotated[dict, Depends(authorization.user_info)]
) -> response.LogoutResultResponse:
    logger.debug("User -> GET -> Logout user")
    usecases.logout(domain.JwtUser.model_validate(user_info))
    return response.LogoutResultResponse(result=str(status.HTTP_200_OK))



async def user_exists_exception_handler(
    request: Request, exception: common.UserAlreadyExists
):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=jsonable_encoder(
            common.GenericHTTPException(
                status_code=str(status.HTTP_409_CONFLICT),
                type="USER_ALREADY_REGISTERED",
                detail=exception.args[0],
            )
        ),
    )


async def user_not_found_exception_handler(
    request: Request, exception: common.UserNotFound
):
    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT,
        content=jsonable_encoder(
            common.GenericHTTPException(
                status_code=str(status.HTTP_204_NO_CONTENT),
                type="USER_NOT_FOUND",
                detail=exception.args[0],
            )
        ),
    )


async def invalid_credentials_exception_handler(
    request: Request, exception: common.InvalidCredentials
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(
            common.GenericHTTPException(
                status_code=str(status.HTTP_400_BAD_REQUEST),
                type="INVALID_CREDENTIALS",
                detail=exception.args[0],
            )
        ),
    )

def user_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(common.UserAlreadyExists, user_exists_exception_handler) # type: ignore
    app.add_exception_handler(common.UserNotFound, user_not_found_exception_handler) # type: ignore
    app.add_exception_handler(common.InvalidCredentials, invalid_credentials_exception_handler) # type: ignore

