from sqlalchemy import Column, Integer, String

from db.connection import Base


class Search(Base):
    __tablename__ = "search_setting"
    
    search_id = Column(String, primary_key=True)
    text = Column(String, nullable=True)
    file_mask = Column(String, nullable=True)
    size_value = Column(Integer, nullable=True)
    size_operator = Column(String, nullable=True)
    creation_time_value = Column(String, nullable=True)
    creation_time_operator = Column(String, nullable=True)
