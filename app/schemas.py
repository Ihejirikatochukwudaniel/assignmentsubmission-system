from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class StudentCreate(BaseModel):
    name: str

class TeacherCreate(BaseModel):
    name: str

class CommentCreate(BaseModel):
    teacher_name: str
    comment: str

class CommentOut(BaseModel):
    id: int
    teacher_name: str
    comment: str
    created_at: datetime

    class Config:
        orm_mode = True

class AssignmentCreate(BaseModel):
    student_name: str
    subject: str
    description: Optional[str] = None

class AssignmentOut(BaseModel):
    id: int
    subject: str
    description: Optional[str]
    file_path: str
    created_at: datetime
    student_name: Optional[str]
    comments: List[CommentOut] = []

    class Config:
        orm_mode = True
