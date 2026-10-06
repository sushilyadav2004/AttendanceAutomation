from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func

from app.database.connection import Base


class ScheduleSetting(Base):
    __tablename__ = "ScheduleSettings"

    Id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    ScheduleName = Column(
        String(100),
        nullable=False
    )

    IntervalMinutes = Column(
        Integer,
        nullable=False
    )

    IsActive = Column(
        Boolean,
        nullable=False,
        default=True
    )

    LastRunAt = Column(
        DateTime,
        nullable=True
    )

    NextRunAt = Column(
        DateTime,
        nullable=True
    )

    CreatedAt = Column(
        DateTime,
        server_default=func.getdate()
    )