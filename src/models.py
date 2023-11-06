from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    alias = Column(String)
    hashed_password = Column(String)
    ts_created = Column(TIMESTAMP(timezone=True), server_default=func.now())
    ts_last_login = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate= func.now())
    is_active = Column(Boolean, default=True)
