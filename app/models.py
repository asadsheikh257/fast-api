from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from .database import Base 
from sqlalchemy.sql import func

class Post(Base):
    __tablename__ = 'Post'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String, index=True)
    published = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
