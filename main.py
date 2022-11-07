from uuid import UUID
from datetime import date
from datetime import datetime
from typing import Optional, List

# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

#FastAPI
from fastapi import FastAPI
from fastapi import status


app = FastAPI()

# Models
## User
class UserBase(BaseModel):
    user_id: UUID = Field(...) #universal unique identifier
    email: EmailStr = Field(...)

class UserLogin(UserBase):
    password: str = Field(
        ..., 
        min_lenght = 8,
        max_lenght = 64
    )

class User(UserBase):
    first_name: str =  Field(
        ...,
        min_length=1, 
        max_length=30
    )
    last_name: str =  Field(
        ...,
        min_length=1, 
        max_length=30
    )
    birth_date: Optional[date] = Field(default = None)

## Tweet
class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ..., 
        min_length=1, 
        max_length = 256
    )
    created_at: datetime = Field(default = datetime.now())
    updated_at: Optional[datetime] = Field(default = None)
    by: User = Field(...)

#Path Operations

## Users
### Register a user
@app.post( # El cliente envía la información del registro
    path = "/signup",
    response_model = User,
    status_code=status.HTTP_201_CREATED,
    summary= "Register a new user",
    tags = ["Users"]
)
def signup():
    pass

### Login a user
@app.post( # El cliente envía la información del registro
    path = "/Login",
    response_model = User,
    status_code=status.HTTP_200_OK,
    summary= "Login a user",
    tags = ["Users"]
)
def Login():
    pass

### Show all users
@app.get( # El cliente envía la información del registro
    path = "/users",
    response_model = List[User],
    status_code=status.HTTP_200_OK,
    summary= "Show all users",
    tags = ["Users"]
)
def users():
    pass

### Show a user
@app.get( # El cliente envía la información del registro
    path = "/users/{user_id}",
    response_model = User,
    status_code=status.HTTP_200_OK,
    summary= "Show a user",
    tags = ["Users"]
)
def show_a_user():
    pass

### Delete a user
@app.delete( # El cliente envía la información del registro
    path = "/users/{user_id}/delete",
    response_model = User,
    status_code=status.HTTP_200_OK,
    summary= "Delete a user",
    tags = ["Users"]
)
def delete_a_user():
    pass

### Update a user
@app.put( # El cliente envía la información del registro
    path = "/users/{user_id}/update",
    response_model = User,
    status_code=status.HTTP_200_OK,
    summary= "Update a user",
    tags = ["Users"]
)
def update_a_user():
    pass


## Tweets
### Show all tweets
@app.get(
    path = "/",  
    response_model = List[Tweet],
    status_code=status.HTTP_200_OK,
    summary= "Show all tweets",
    tags = ["Tweets"])
def home():
    return {"Primitive Twitter": "Working"}

### Post a tweet
@app.post(
    path = "/post",
    response_model = Tweet,
    status_code=status.HTTP_201_CREATED,
    summary= "Post a tweet",
    tags = ["Tweets"]
)
def post():
    pass

### Show a tweet
@app.get(
    path = "/tweets/{tweet_id}",
    response_model = Tweet,
    status_code=status.HTTP_200_OK,
    summary= "Show a tweet",
    tags = ["Tweets"]
)
def show_a_tweet():
    pass

### Delete a tweet
@app.delete(
    path = "/tweets/{tweet_id}/delete",
    response_model = Tweet,
    status_code=status.HTTP_200_OK,
    summary= "Delete a tweet",
    tags = ["Tweets"]
)
def delete_a_tweet():
    pass

### Update a tweet
@app.put(
    path = "/tweets/{tweet_id}/update",
    response_model = Tweet,
    status_code=status.HTTP_200_OK,
    summary= "Update a tweet",
    tags = ["Tweets"]
)
def update_a_tweet():
    pass