import uuid
from sciuromorpha_core.db.base_class import Base, SerializerMixin
from sqlalchemy import Column, Identity
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, String, JSON
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import OID, UUID, BIT, ARRAY


class Meta(Base, SerializerMixin):
    serialize_rules = ("-tasks",)

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, unique=True, default=uuid.uuid4)
    data = Column(JSON(none_as_null=True))
    origin_url = Column(String, index=True, unique=True)
    process_tag = Column(ARRAY(String, dimensions=1))

    tasks = relationship("Task", back_populates="meta")
