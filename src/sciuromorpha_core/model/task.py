from .base import Base
from sqlalchemy import Column, Identity
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, String, JSON, BINARY
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import OID, UUID, BIT, ARRAY, ENUM


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, Identity(cycle=True), primary_key=True)
    meta_id = Column(UUID(as_uuid=True), ForeignKey("meta.id"))
    worker = Column(String)
    param = Column(BINARY)
    status = Column(
        ENUM("pending", "waiting", "running", "success", "failed", name="task-status")
    )
