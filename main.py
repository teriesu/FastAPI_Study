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
@app.get(path = "/")
def home():
    return {"Primitive Twitter": "Working"}

## Users
@app.post( # El cliente envía la información del registro
    path = "/signup",
    response_model = User,
    status_code=status.HTTP_201_CREATED,
    summary= "Register a new user",
    tags = ["Users"]
)
def signup():
    pass

@app.post( # El cliente envía la información del registro
    path = "/Login",
    response_model = User,
    status_code=status.HTTP_200_OK,
    summary= "Login a user",
    tags = ["Users"]
)
def Login():
    pass

@app.get( # El cliente envía la información del registro
    path = "/users",
    response_model = List[User],
    status_code=status.HTTP_200_OK,
    summary= "Show all users",
    tags = ["Users"]
)
def users():
    pass

@app.get( # El cliente envía la información del registro
    path = "/users/{user_id}",
    response_model = User,
    status_code=status.HTTP_200_OK,
    summary= "Show a user",
    tags = ["Users"]
)
def show_a_user():
    pass

@app.delete( # El cliente envía la información del registro
    path = "/users/{user_id}/delete",
    response_model = User,
    status_code=status.HTTP_200_OK,
    summary= "Delete a user",
    tags = ["Users"]
)
def delete_a_user():
    pass



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