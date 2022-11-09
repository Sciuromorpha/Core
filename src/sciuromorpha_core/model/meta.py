import uuid
from .base import Base
from sqlalchemy import Column, Identity
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, String, JSON
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import OID, UUID, BIT, ARRAY

class Meta(Base):
    __tablename__ = "meta"

    id = Column(UUID(as_uuid=True), Identity(), primary_key=True, default=uuid.uuid4)
    meta = Column(JSON(none_as_null=True))
    origin_url = Column(String)
    process_tag = Column(ARRAY(String, dimensions=1))