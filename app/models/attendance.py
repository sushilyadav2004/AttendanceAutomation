from sqlalchemy import Column, Integer, String, Date, Time, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.database.connection import Base


class Attendance(Base):
    __tablename__ = "Attendance"

    Id = Column(Integer, primary_key=True, index=True)

    EmployeeId = Column(
        String(50),
        ForeignKey("Employees.EmployeeId"),
        nullable=False
    )

    AttendanceDate = Column(Date, nullable=False)

    Status = Column(String(20), nullable=False)

    LoginTime = Column(Time, nullable=True)

    LogoutTime = Column(Time, nullable=True)

    SourceFile = Column(String(255), nullable=True)

    CreatedAt = Column(
        DateTime,
        server_default=func.getdate()
    )