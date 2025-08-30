from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from repository.request import (
    admin_get_requests,
    create_request,
    get_single_request,
    get_states,
    requester_get_requests,
    update_request,
)
from model import model
from model.schemas import *
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from sqlalchemy import update, desc
from datetime import time

from util.util import *


router = APIRouter(tags=["requests"], prefix="/requests")


@router.get("/requester-requests/", response_model=List[RequestResponse])
async def requester_read_requests(
    current_user: Annotated[UserInfoResponse, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 10,
    info: str = None,
    db: Session = Depends(get_db),
):
    requests = requester_get_requests(
        db, skip=skip, limit=limit, info=info, user_id=current_user.id
    )
    return requests


@router.get("/admin-requests/", response_model=List[RequestResponse])
async def admin_read_requests(
    skip: int = 0,
    limit: int = 10,
    info: str = None,
    db: Session = Depends(get_db),
):
    requests = admin_get_requests(db, skip=skip, limit=limit, info=info)
    return requests


@router.post("/requests/", response_model=RequestResponse)
async def add_request(request: RequestAddRequest, db: Session = Depends(get_db)):
    return create_request(db=db, request=request)


@router.put("/request/{request_id}", response_model=RequestResponse)
async def edit_request(
    request_id: int, request_update: RequestUpdate, db: Session = Depends(get_db)
):
    return update_request(db=db, request_id=request_id, request_update=request_update)


@router.get("/states/", response_model=List[StateResponse])
async def read_states(
    db: Session = Depends(get_db),
):
    states = get_states(db=db)
    if not states:
        raise HTTPException(status_code=404, detail="No states found")
    return states


@router.get("/single-request/{request_id}", response_model=RequestResponse)
async def read_single_request(request_id: int, db: Session = Depends(get_db)):
    request = get_single_request(db=db, request_id=request_id)
    if not request:
        raise HTTPException(status_code=404, detail="No request found")
    return request


# ///////////////////  GET REQUEST SINGLE REQURE
