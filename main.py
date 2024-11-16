from fastapi import Body, FastAPI, HTTPException, status, Response
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str 
    content: str
    published: bool = True
    rating: Optional[int] = None

my_post = [{"title":"title of post 1", "content":"content of post 1", "id":1},
           {"title":"title of post 2", "content":"content of post 2", "id":2}]

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_post():
    return {'data':my_post}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0,1000000000)
    my_post.append(post_dict)
    return {'data': post_dict}

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

@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id:{id} does not exist.')
    post_dict = post.model_dump()
    post_dict['id'] = id 
    my_post[index] = post_dict
    return {'message': 'Post Updated'}
