from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String)  # 'HOD', 'Staff', 'Rep'
    assigned_year = Column(String, nullable=True) # Used for Reps e.g., '2nd_year', '3rd_year'

    logs = relationship("LateLog", back_populates="logged_by_user")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    register_no = Column(String, unique=True, index=True)
    name = Column(String)
    year = Column(String) # '2nd_year', '3rd_year', '4th_year'
    semester = Column(String)
    batch = Column(String)

    late_logs = relationship("LateLog", back_populates="student")


class LateLog(Base):
    __tablename__ = "late_logs"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    date = Column(Date)
    time = Column(Time)
    session = Column(String) # 'Morning', 'After Break', 'After Lunch'
    logged_by_id = Column(Integer, ForeignKey("users.id"))
    
    student = relationship("Student", back_populates="late_logs")
    logged_by_user = relationship("User", back_populates="logs")
