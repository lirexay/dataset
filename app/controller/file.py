from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page, Params
from api.deps import get_files_service
from core.auth import get_current_user

from schema.auth import UserInfoResponse
from schema.response import StandardResponse, success
from schema.file import FileCreate, FileOut, FileUpdate
from service.file import FilesService
import os
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
router = APIRouter()


# @router.post("/", response_model=StandardResponse[FileOut], status_code=status.HTTP_201_CREATED)
# async def create_file(
#     payload: FileCreate,
#     service: FilesService = Depends(get_files_service)
# ):
#     return success(await service.create_file(payload))

ALLOWED_EXTENSIONS = {"csv", "xlsx", "xls",
                      "json", "txt", "pdf"}  # customize as needed


def file_extension_allowed(file_extension: str):
    if file_extension.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, detail="File extension not allowed!")


def compute_file_hash(filename: str) -> str:
    import hashlib
    hash_input = f"{filename}".encode()
    return hashlib.sha256(hash_input).hexdigest()


async def write_file_to_disk(file_name: str, file: UploadFile) -> str:
    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", file_name)
    with open(file_path, "wb") as f:
        while chunk := await file.read(1024 * 1024):  # 1 MB chunks
            f.write(chunk)
    return file_path


@router.post(
    "/upload/",
    response_model=StandardResponse[FileOut],
    status_code=status.HTTP_201_CREATED,
    summary="Upload a new file"
)
async def upload_file(

    file: UploadFile = File(...),
    service: FilesService = Depends(get_files_service),
):
    # Extract file extension
    filename = file.filename
    if not filename:
        raise HTTPException(status_code=400, detail="File has no name")

    _, ext = os.path.splitext(filename)
    file_extension = ext[1:].lower()  # remove leading dot

    # Validate extension
    file_extension_allowed(file_extension)

    # Generate unique file name
    file_hash = compute_file_hash(filename)
    stored_filename = f"{file_hash}.{file_extension}"

    # Save file to disk
    await write_file_to_disk(stored_filename, file)

    # Create DB record via service
    file_create_payload = {"name": stored_filename}
    db_file = await service.create_file(file_create_payload)

    return success(db_file)


@router.get("/{file_id}", response_model=StandardResponse[FileOut])
async def read_file(file_id: int, service: FilesService = Depends(get_files_service)):
    obj = await service.get_file(file_id)
    if not obj:
        raise HTTPException(status_code=404, detail="File not found")
    return success(obj)
