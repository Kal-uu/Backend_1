from typing import Optional

from pydantic import BaseModel
from fastapi import UploadFile, Form


class ProjectCreate(BaseModel):
    title: str
    description: str


class ProjectResponse(ProjectCreate):
    id: int
    image: Optional[str]
    video: Optional[str]

    class Config:
        from_attributes = True
