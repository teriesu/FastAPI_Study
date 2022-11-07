from uuid import UUID
from datetime import date
from datetime import datetime
from typing import Optional, List
import json

# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

#FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body
from fastapi import HTTPException


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

class UserRegister(User):
    password: str = Field(
        ..., 
        min_lenght = 8,
        max_lenght = 64
    )

## Tweet
class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ..., 
        min_length=1, 
        max_length=256
    )
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
    by: UserBase = Field(...)

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
def signup(user: UserRegister =  Body(...)):
    """
    This path operation register a user in the app

    Parameters:
    - Request body parameter
        - user: UserRegister
    
    Returns a json with the basic user information:
    - user_id: uuid
    - email: Emailstr
    - first_name: str
    - last_name: str
    - birth_date: str
    """    
    with open("users.json", "r+", encoding = "utf-8") as f:
        results = json.load(f)
        user_dict = user.dict()
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        if any(str(users['user_id']) == str(user.user_id) for users in results):
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User ID already exist!"
        )
        if any(users['email'] == user.email for users in results):
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exist!"
        )
        results.append(user_dict)
        f.seek(0) #Regreso al primer byte
        f.write(json.dumps(results, indent=2))
        return user


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
def show_all_users():
    '''
    This path operation shows all users created in the app

    Parameters: 
    - None

    Returns a list with the basic user information of all users created in the app:
    - user_id: UUID
    - email: Emailstr
    - first_name: str
    - last_name: str
    - birth_date: date

    '''
    with open("users.json", "r", encoding = "utf-8") as f:
        results = json.loads(f.read())
        return results


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
    path="/",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all tweets",
    tags=["Tweets"]
)
def show_all_tweets():
    '''
    This path operation shows all users created in the app

    Parameters: 
    - None

    Returns a list with the basic user information of all users created in the app:
    - user_id: UUID
    - email: Emailstr
    - first_name: str
    - last_name: str
    - birth_date: date

    '''
    with open("users.json", "r", encoding = "utf-8") as f:
        results = json.loads(f.read())
        return results
        
# @app.get(
#     path = "/",  
#     response_model = List[Tweet],
#     status_code=status.HTTP_200_OK,
#     summary= "Show all tweets",
#     tags = ["Tweets"])
# def home():

#     with open("users.json", "r", encoding = "utf-8") as f:
#         results = json.loads(f.read())
#         return results

### Post a tweet
@app.post(
    path = "/post",
    response_model = Tweet,
    status_code=status.HTTP_201_CREATED,
    summary= "Post a tweet",
    tags = ["Tweets"]
)
def post(tweet: Tweet =  Body(...)):
    '''
    Post a Tweet

    This path operation post a Tweet in the app
    
    Parameters:
    - Request Body parameter
        - tweet: Tweet
    
    Returns a JSON with the basic tweet information:
    - tweet_id: UUID
    - content: str
    - created_at: datetime
    - updated_at: Optional[datetime]
    - by: User
    '''
    with open("tweets.json", "r+", encoding = "utf-8") as f:
        results = json.load(f)
        tweet_dict = tweet.dict()
        tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
        tweet_dict["created_at"] = str(tweet_dict["created_at"])
        if tweet_dict["updated_at"]:
            tweet_dict["updated_at"] = str(tweet_dict["updated_at"])
        tweet_dict["by"]["user_id"] = str(tweet_dict["by"]["user_id"])
        if any(str(tweets['tweet_id']) == str(tweet.tweet_id) for tweets in results):
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Tweet ID already exist!"
        )
        results.append(tweet_dict)
        f.seek(0) #Regreso al primer byte
        f.write(json.dumps(results, indent=4))
        return tweet

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