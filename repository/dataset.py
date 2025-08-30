from sqlalchemy.orm import Session
from model.model import *
from model.schemas import *


def get_datasets(db: Session, skip: int = 0, limit: int = 10, info: str = None):
    query = db.query(Dataset)
    if info:
        query = query.filter(Dataset.name.ilike(f"%{info}%"))
    return query.offset(skip).limit(limit).all()


def get_single_dataset(db: Session, dataset_id: int):
    return db.query(Dataset).filter(Dataset.id == dataset_id).first()
