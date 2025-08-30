from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response

from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from datetime import time

from repository.dataset import get_datasets, get_single_dataset

from repository.request import *

from repository.user import *

from util.util import *


router = APIRouter(tags=["dataset"], prefix="/dataset")


@router.get("/datasets/", response_model=List[DatasetLimitedResponse])
async def read_datasets(
    skip: int = 0, limit: int = 10, info: str = None, db: Session = Depends(get_db)
):
    datasets = get_datasets(db, skip=skip, limit=limit, info=info)
    return datasets


@router.get("/single-dataset/{dataset_id}", response_model=DatasetResponse)
async def read_dataset(dataset_id: int, db: Session = Depends(get_db)):
    proposal = get_single_dataset(db=db, dataset_id=dataset_id)
    return proposal
