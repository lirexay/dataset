from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.exceptions import ValidationException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel

from api.deps import get_auth_service, get_users_service
from core.auth import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)
from core.config import settings
import schema
from schema.auth import PasswordResetConfirm, PasswordResetRequest, Token, UserCreate, UserInfoResponse, UserOut
from schema.response import StandardResponse, success
from service.auth import AuthService
from service.user import UsersService
from utils.email import send_reset_password_email

router = APIRouter()


# Mock user DB (replace with real DB in production)
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "hashed_password": get_password_hash("secret"),
    }
}


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


@router.post(
    "/signup",
    response_model=StandardResponse[UserOut],
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user"
)
async def signup(
    user_in: UserCreate,
    service: UsersService = Depends(get_users_service)
):
    try:
        user = await service.create_user(user_in)
        return success(user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )


@router.post(
    "/password-reset/request",
    response_model=StandardResponse[str],
    summary="Request password reset"
)
async def request_password_reset(
    data: PasswordResetRequest,
    service: UsersService = Depends(get_users_service)
):
    token = await service.initiate_password_reset(data.username)
    if token:
        # In real app: fetch user.email and send email
        # using username as placeholder
        send_reset_password_email(data.username, token)
    # Always return success (to avoid user enumeration)
    return success("اگر نام کاربری معتبر باشد، ایمیل بازنشانی ارسال شده است.")


@router.post(
    "/password-reset/confirm",
    response_model=StandardResponse[bool],
    summary="Confirm password reset"
)
async def confirm_password_reset(
    data: PasswordResetConfirm,
    service: UsersService = Depends(get_users_service)
):
    success_reset = await service.reset_password(data.token, data.new_password)
    if not success_reset:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="توکن نامعتبر یا منقضی شده است."
        )
    return success(True)


@router.post(
    "/login", response_model=Token
)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 service: AuthService = Depends(get_auth_service),):

    user = await service.get_user(username=form_data.username,
                                  password=get_password_hash(form_data.password))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(user.password, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        claims={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/me", )
async def read_users_me(current_user: Annotated[UserInfoResponse, Depends(get_current_user)],):
    print(current_user.id)
    return current_user


# @router.get("/protected")
# async def protected_route(current_user: dict = Depends(get_current_user)):
#     return {"message": f"Hello {current_user['username']}, you are authenticated!"}
