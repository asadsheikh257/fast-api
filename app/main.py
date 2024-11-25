from fastapi import Body, FastAPI, HTTPException, status, Response, Depends
from pydantic import BaseModel
from typing import Optional, List, Annotated
from random import randrange
import psycopg
from fastapi.responses import JSONResponse


from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, Base, get_db
# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI()

# class Post(BaseModel):
#     title: str 
#     content: str
#     published: bool = True


my_post = [{"title":"title of post 1", "content":"content of post 1", "id":1},
           {"title":"title of post 2", "content":"content of post 2", "id":2}]

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts", response_model=List[schemas.Post])
def get_post(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    post = db.query(models.Post).offset(skip).limit(limit).all()
    if not post:  # Check if the list is empty
        return JSONResponse(content={"message": "There is no data"}, status_code=200)
    return db.query(models.Post).offset(skip).limit(limit).all()


@app.post('/posts', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    db_post = models.Post(**post.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def find_posts(id):
    for p in my_post:
        if p['id'] == id:
            return p

@app.get('/posts/{id}')
def get_post(id: int):
    post = find_posts(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id:{id} was not found.')
    return {'find_post': post}

def find_index(id):
    for i ,p in enumerate(my_post):
        if p['id'] == id:
            return i

@app.delete('/posts/{id}')
def delete_post(id: int):
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id:{id} does not exist.')
    my_post.pop(index)
    return Response(status_code=status.HTTP_404_NOT_FOUND)

# @app.put('/posts/{id}')
# def update_post(id: int, post: Post):
#     index = find_index(id)
#     if index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f'Post with id:{id} does not exist.')
#     post_dict = post.model_dump()
#     post_dict['id'] = id 
#     my_post[index] = post_dict
#     return {'message': 'Post Updated'}
