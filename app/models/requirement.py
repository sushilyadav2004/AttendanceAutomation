from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func

from app.database.connection import Base


class Requirement(Base):
    __tablename__ = "Requirements"

    Id = Column(Integer, primary_key=True, index=True)

    RuleName = Column(
        String(150),
        nullable=False
    )

    ColumnName = Column(
        String(100),
        nullable=False
    )

    Operator = Column(
        String(20),
        nullable=False
    )

    ExpectedValue = Column(
        String(255),
        nullable=True
    )

    IsActive = Column(
        Boolean,
        nullable=False,
        default=True
    )

    CreatedAt = Column(
        DateTime,
        server_default=func.getdate()
    )