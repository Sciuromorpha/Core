from sciuromorpha_core.db.base_class import Base
from sqlalchemy import Column, Identity
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, String, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import OID, UUID, BIT, ARRAY, ENUM, BYTEA


class Task(Base):
    serialize_rules = ("-meta",)

    id = Column(Integer, Identity(cycle=True), index=True, unique=True, primary_key=True)
    meta_id = Column(UUID(as_uuid=True), ForeignKey("meta.id"))
    worker = Column(String)
    param = Column(BYTEA)
    status = Column(
        ENUM("pending", "waiting", "running", "success", "failed", name="task-status")
    )

    meta = relationship("Meta", back_populates="tasks")
