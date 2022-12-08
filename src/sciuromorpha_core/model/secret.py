from sciuromorpha_core.db.base_class import Base, SerializerMixin
from sqlalchemy import Column, Identity, Index
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, String, JSON
from sqlalchemy.orm import relationship


class Secret(Base, SerializerMixin):
    # serialize_rules = ("-data",)

    id = Column(
        Integer, Identity(cycle=True), index=True, unique=True, primary_key=True
    )
    service = Column(String)
    key = Column(String)
    data = Column(JSON(none_as_null=True))

    __table_args__ = (Index("ix_ssk", "service", "key", unique=True),)
