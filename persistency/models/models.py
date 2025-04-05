from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, SmallInteger, String

from persistency.connection import Base
from utils.helpers.time_helpers.utc_to_local import utc_to_local


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String)
    created_at = Column(DateTime, default=lambda: utc_to_local(datetime.utcnow()))
    deleted_at = Column(DateTime)
    updated_at = Column(DateTime, onupdate=lambda: utc_to_local(datetime.utcnow()))
    role = Column(String)
    status = Column(SmallInteger, nullable=False, default=0)
