import uuid
from sciuromorpha_core.db.base_class import Base
from sqlalchemy import Column, Identity
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, String, JSON
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import OID, UUID, BIT, ARRAY


class Meta(Base):
    __tablename__ = "meta"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    meta = Column(JSON(none_as_null=True))
    origin_url = Column(String)
    process_tag = Column(ARRAY(String, dimensions=1))

    tasks = relationship("Task", back_populates="meta")
