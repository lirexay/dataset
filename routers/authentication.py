from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, status
from sqlalchemy.orm import Session
from model import model, schemas
from util import util
from util.util import *
from sqlalchemy.orm import Session
from typing import Annotated

router = APIRouter(tags=["authentication"])


@router.post("/token", response_model=schemas.Token)
async def login(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(model.User).filter(
        model.User.username == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="invalid username"
        )

    if not verify_hash(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="invalid username"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
        "role_id": user.user_type_id,
    }


@router.post("/refresh-token", response_model=schemas.Token)
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db),
):
    payload = verify_token(refresh_token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": payload["sub"]})
    new_refresh_token = create_refresh_token(data={"sub": payload["sub"]})
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": new_refresh_token,
        "role_id": user.user_type_id,
    }


@router.get("/users/me", response_model=schemas.UserMeInfoResponse)
async def read_users_me(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    db: Session = Depends(get_db),
):

    user = db.query(model.User).filter(
        model.User.id == current_user.id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return schemas.UserMeInfoResponse(
        id=user.id,
        username=user.username,
        fname=user.fname,
        lname=user.lname,
        phone=user.phone,
    )


@router.post("/chane-pass/")
def change_pass(current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)], password: schemas.UserChangePassword, db: Session = Depends(get_db),):
    user = db.query(User).filter(User.phone == current_user.phone).first()
    user.password = password.password
    db.commit()
    db.refresh(user)


@router.post("/signup/")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=400, detail="Username already registered")

    existing_user = db.query(User).filter(User.phone == user.phone).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Phone already registered")

    new_user = User(
        fname=user.fname,
        lname=user.lname,
        username=user.username,
        password=util.hash(user.password),
        phone=user.phone,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
