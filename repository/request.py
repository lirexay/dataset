from sqlalchemy.orm import Session
from model.model import *
from model.schemas import *
from fastapi import HTTPException


def create_request(db: Session, request: RequestAddRequest, user_id: int):
    db_request = Request(
        user_requestor_id=user_id,
        title=request.title,
        description=request.description,
        comment=request.comment,
        state_id=request.state_id,
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request


def requester_get_requests(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    info: str = None,
):
    query = db.query(Request)
    if info:
        query = query.filter(
            Request.title.ilike(f"%{info}%") & Request.user_requestor_id == user_id
        )
    return query.offset(skip).limit(limit).all()


def admin_get_requests(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    info: str = None,
):
    query = db.query(Request)
    if info:
        query = query.filter(Request.title.ilike(f"%{info}%"))
    return query.offset(skip).limit(limit).all()


def update_request(db: Session, request_id: int, request_update: RequestUpdate):
    request = db.query(Request).filter(Request.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="request not found")

    request.state = request_update.state
    request.comment = request_update.comment

    db.commit()
    db.refresh(request)
    return request


def get_single_request(db: Session, request_id: int):
    return db.query(Request).filter(Request.id == request_id).first()


def get_states(db: Session):
    return db.query(State).all()
