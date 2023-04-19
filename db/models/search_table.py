import uuid

from sqlalchemy import Column, Integer, String, DateTime

from db.connection import Base


class Search(Base):
    __tablename__ = "search_settings"
    
    search_id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    text = Column(String, nullable=True)
    file_mask = Column(String, nullable=True)
    size_value = Column(Integer, nullable=True)
    size_operator = Column(String, nullable=True)
    creation_time_value = Column(DateTime, nullable=True)
    creation_time_operator = Column(String, nullable=True)
