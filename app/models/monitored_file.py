from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.sql import func

from app.database.connection import Base


class MonitoredFile(Base):
    __tablename__ = "MonitoredFiles"

    Id = Column(Integer, primary_key=True, index=True)

    FileName = Column(
        String(255),
        nullable=False
    )

    FilePath = Column(
        String(500),
        nullable=False
    )

    FileDate = Column(
        Date,
        nullable=True
    )

    ProcessedAt = Column(
        DateTime,
        nullable=True
    )

    Status = Column(
        String(30),
        nullable=False,
        default="Pending"
    )

    CreatedAt = Column(
        DateTime,
        server_default=func.getdate()
    )