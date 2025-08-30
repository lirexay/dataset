from datetime import datetime, timedelta, timezone
import hashlib
import random

from fastapi import Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session
from jwt.exceptions import InvalidTokenError
from model import database
from fastapi.security import OAuth2PasswordBearer
import jwt
from typing import Optional
from passlib.context import CryptContext
import yaml

from model.model import User

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """
    
    I'm well aware of security problem with my SECRET_KEY implementation
      I have done it like this for the sake of easy initialization of 
      backend for Javad.
      The SECRET_KEY will be changed after Javad is done with the front.


 """ """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""


SECRET_KEY = "09d15e094aaa6ca2556c518166b7a9563b93f7099f6f0f4caa6cf45b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7
FILE_HASH_KEY = "09d15e094aaa6ca2556c518166b7a9563b93f7099f6f0f4caa6cf45b88e8d3e7"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# file
def load_allowed_extensions(yaml_file):
    with open(yaml_file, "r") as file:
        return yaml.safe_load(file)["allowed_extensions"]


def compute_file_hash(user_id: str, file_name: str) -> str:
    key = FILE_HASH_KEY
    random_int = random.randint(1, 10000)
    hash_input = f"{user_id}{key}{random_int}{file_name}".encode("utf-8")
    return hashlib.sha256(hash_input).hexdigest()


# database


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close_all()


# user


def hash(password):

    hashed_password = pwd_context.hash(password)
    return hashed_password


def verify_hash(hashed_password, plain_password):
    return pwd_context.verify(plain_password, hashed_password)


# login


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = db.query(User).filter(User.username == username).first()
        return user
    except InvalidTokenError:
        raise credentials_exception
