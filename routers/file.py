from fastapi import APIRouter, Depends, HTTPException, responses, File, UploadFile
from service.file import *
from model.schemas import *
from sqlalchemy.orm import Session
import os
from repository.file import *
from util.util import *
from pathlib import Path

# ALLOWED_EXTENSIONS = load_allowed_extensions("allowed_extensions.yaml")

# ALLOWED_EXTENSIONS = {"pdf", "docx", "pptx"}
# KEY = "a234slkdjfgosdi547utbod7sinfl87cvdiyrstn4bol3asuy8d"  # will be changed
router = APIRouter(tags=["file"], prefix="/file")


@router.post("/upload/")
async def upload_file(
    current_user: Annotated[UserInfoResponse, Depends(get_current_user)],
    file: UploadFile,
    db: Session = Depends(get_db),
):
    user_id = current_user.id
    access_id = current_user.user_role_id
    file_extension = os.path.splitext(file.filename)[1][1:]
    file_extension_allowed(file_extension)

    file_hash = compute_file_hash(user_id, file.filename)
    file_name = file_hash + "." + file_extension
    file_ = await write_file_hash(file_name=file_name, file=file)
    return file_create_file(
        db=db,
        file_hash=file_name,
        access_id=access_id,
        # access_id=access_id
    )


@router.get("/download/{file_id}")
async def download_file(file_id: int, db: Session = Depends(get_db)):
    db_file = db.query(File).filter(File.id == file_id).first()
    db_file_exist(db_file)
    upload_dir = os.path.abspath("uploads")
    safe_file_name = Path(db_file.name).name
    file_path = os.path.join(upload_dir, safe_file_name)

    if not os.path.exists(file_path):
        return {"error": "File does not exist"}

    return responses.FileResponse(
        path=file_path, filename=safe_file_name, media_type="application/octet-stream"
    )


@router.get("/files")
async def get_file_ids(db: Session = Depends(get_db)):
    return get_all_files(db)
