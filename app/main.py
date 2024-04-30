import os

from fastapi import FastAPI, HTTPException, status
from uuid import uuid4
from redis import Redis
from pydantic import BaseModel

app = FastAPI(
    title='fastapi + reids',
    docs_url='/'
)

r = Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), charset="utf-8", decode_responses=True)

class User(BaseModel):
    name: str
    age: int
    
    
class UserDatabase(User):
    id: str = str(uuid4())


@app.post(
    '/user',
    status_code=status.HTTP_201_CREATED,
    response_model=UserDatabase,
    response_model_by_alias=False
    )
async def set_data(user: User):
    user_database = UserDatabase(**(user.model_dump()))
    r.hset(str(user_database.id), mapping=user_database.model_dump())
    return user_database


@app.get(
    '/user/{id}',
    status_code=status.HTTP_200_OK,
    response_model=User,
    response_model_by_alias=False
    )
async def get_data(id: str):
    data = r.hgetall(id)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return data


@app.delete(
    '/user/{id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_data(id: str):
    r.delete(id)
    