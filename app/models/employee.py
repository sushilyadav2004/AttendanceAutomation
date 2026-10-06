from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func

from app.database.connection import Base


class Employee(Base):
    __tablename__ = "Employees"

    Id = Column(Integer, primary_key=True, index=True)
    EmployeeId = Column(String(50), unique=True, nullable=False)
    EmployeeName = Column(String(150), nullable=False)
    Department = Column(String(100), nullable=True)
    IsActive = Column(Boolean, default=True)
    CreatedAt = Column(DateTime, server_default=func.getdate())