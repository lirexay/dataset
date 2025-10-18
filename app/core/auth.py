from datetime import datetime, timedelta
from typing import Annotated, AsyncGenerator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt

from sqlalchemy.ext.asyncio import AsyncSession
# from api import deps
from db.session import get_db

from core.config import settings
from entities.user import User
from service.auth import AuthService


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login", auto_error=True)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_password_reset_token(username: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": username, "type": "password_reset"}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_access_token(claims: dict, expires_delta: Optional[timedelta] = None) -> str:
    claims_to_encode = claims.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    claims_to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        claims_to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


async def get_auth_service(
    db: AsyncSession = Depends(get_db),
) -> AsyncGenerator[AuthService, None]:
    yield AuthService(db)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    service: AuthService = Depends(get_auth_service),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:

        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")

        if username is None:

            raise credentials_exception
        print(3, "  ", username)
        user = await service.get_user_by_username(username=username)

    except JWTError:
        raise credentials_exception
    return user


# Optional: You can create a dependency that returns the actual user object
# async def get_current_active_user(current_user: dict = Depends(get_current_user)):
#     # Add logic to check if user is active, etc.
#     return current_user
