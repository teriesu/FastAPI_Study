from uuid import UUID
from datetime import date
from datetime import datetime
from typing import Optional

# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

#FastAPI
from fastapi import FastAPI


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