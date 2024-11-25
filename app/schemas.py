from pydantic import BaseModel 
from datetime import datetime

class PostBase(BaseModel):
    title: str 
    content: str
    published: bool = True
    created_at : datetime

class PostCreate(PostBase):
    pass 

class Post(PostBase):
    id: int 

    class Config: 
        from_attributes = True