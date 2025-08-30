from sqlalchemy.sql import exists
from sqlalchemy.orm import Session
from model.model import *
from model.schemas import *
from fastapi import HTTPException


def file_create_file(
    db: Session,
    file_hash: str,
    access_id: int,
):
    db_file = File(info=file_hash, access_id=access_id)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


def get_all_files(db: Session):
    return db.query(File).all()
