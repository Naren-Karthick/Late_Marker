from pydantic import BaseModel
from typing import List, Optional
from datetime import date, time

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    username: str
    assigned_year: Optional[str] = None

class TokenData(BaseModel):
    username: Optional[str] = None

class UserBase(BaseModel):
    username: str
    role: str

class UserCreate(UserBase):
    password: str
    assigned_year: Optional[str] = None

class User(UserBase):
    id: int
    assigned_year: Optional[str] = None
    
    class Config:
        from_attributes = True

class StudentBase(BaseModel):
    register_no: str
    name: str
    year: str
    semester: str
    batch: str

class Student(StudentBase):
    id: int

    class Config:
        from_attributes = True

class LateLogCreate(BaseModel):
    student_ids: List[int]
    date: date
    time: str # We'll parse to time obj
    session: str

class LateLog(BaseModel):
    id: int
    student_id: int
    date: date
    time: time
    session: str
    logged_by_id: int
    
    class Config:
        from_attributes = True

class LateLogDetailed(LateLog):
    student: Student
    logged_by_user: User
    
    class Config:
        from_attributes = True
