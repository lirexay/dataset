from pydantic import BaseModel


class FileBase(BaseModel):
    name: str


class FileCreate(FileBase):
    pass


class FileUpdate(FileBase):
    pass


class FileOut(FileBase):
    id: int

    class Config:
        from_attributes = True
