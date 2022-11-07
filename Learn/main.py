#Python
from typing import Optional, List
from fastapi.params import Path
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr, HttpUrl, PaymentCardNumber

# FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path, Form, Header, Cookie, UploadFile, File
from fastapi import status
from fastapi import HTTPException

app = FastAPI()

# Models

class HairColor(Enum):
    white = 'white'
    black = 'black'
    blonde = 'blonde'
    brown = 'brown'
    red = 'red'

class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=4,
        max_length=24,
        example="Montevideo"
        )
    state: str = Field(
        ...,
        min_length=4,
        max_length=24,
        example="Montevideo"
        )
    country: str = Field(
        ...,
        min_length=4,
        max_length=24,
        example="Uruguay"
        )
    latam: bool = Field(example=True)

class PersonBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length=3,
        max_length=35,
        example="Santiago"
        )
    last_name: str = Field(
        ...,
        min_length=3,
        max_length=35,
        example="Téllez"
        )
    age_person: int = Field(
        ...,
        ge=18,
        le=115,
        example=39
        )
    color_hair: Optional[HairColor] = Field(default=None, example=HairColor.black)
    married: Optional[bool] = Field(default=None, example=True)
    email_usr : EmailStr = Field(default=None, example="santiago99tellez@hotmail.com")
    web_usr : HttpUrl = Field(default=None, example="https://www.gmail.com")

class Person(PersonBase): # Person parameters
    pay_card_usr: PaymentCardNumber = Field(default=None, example="5158459994949763")
    password: str = Field(..., min_length=8)

class PersonOut(PersonBase):
    pass

class LoginOut(BaseModel):
    username: str = Field(
    ..., 
    max_lenght = 20, 
    example = "santiago2022"
    )

@app.get(
    path = "/", 
    status_code = status.HTTP_200_OK
    ) #Path operation decorator
def home(): #Path operation function
    return {"First API": "Congratulation"} #JSON

# Request and Response Body

@app.post(
    path = "/person/new", 
    response_model = PersonOut,
    status_code= status.HTTP_201_CREATED,
    tags = ["Persons"], 
    summary = "Create Person in the app"
    ) # Acces a new person
def create_person(person: Person = Body(...)): # acces to the parameters of person
    """
    - Titulo
    - Descripción
    - Parámetros
    - Resultado

    Create person

    This path operation creates a person in the app and save the information in the database

    Parameters: 
    - Request body Parameter:
        - **person: Person** -> A person model with first name, last name, age, hair color and marital status

    Returns a person model with first name, last name, age, hair color and marital status
    """
    return person

# Validations: Query Parameters

@app.get(
    path = "/person/detail",
    status_code= status.HTTP_200_OK,
    tags = ["Persons"],
    deprecated = True
    )
def show_person(
    name: Optional[str] = Query(
        None, 
        min_length=3, 
        max_length=35,
        title="Person Name",
        description="This is the person name. It's between 3 and 35 characters.",
        example="Pedro"
        ),
    age: str = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required.",
        example="34"
        )
    ):
    """
    Show person 

    This path operation recibe the person's information and it shows it
    """    
    return {name: age}

# Validations: Path Parameters
persons = [1, 2, 3, 4, 5] # IDs existentes para la comprobación

@app.get(
    path = "/person/detail/{person_id}", 
    status_code = status.HTTP_200_OK,
    tags = ["Persons"]
    )
def show_person(
    person_id: int = Path(
        ..., 
        gt=0,
        title="Person ID",
        description="This is the person ID. It's reqiuired and it's more than 0.",
        example=300
        )
    ):
    if person_id not in persons:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "This person doesn't exist"
        )
    else:
        return {person_id: "it_exist!"}

# Validations: Request Body
@app.put(
    path = "/person/{person_id}",
    status_code = status.HTTP_200_OK,
    tags = ["Persons"]
    )
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0,
        example=300
    ),
    person: Person = Body(...),
    location: Location = Body(...),
    tags = ["Persons"]
):
    results = person.dict()
    results.update(location.dict())
    return results 

@app.post(
    path = "/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags = ["Persons"]
    )
def login(
    username: str = Form(...), 
    password: str = Form(...)
    ):
    return LoginOut(username = username)

# Cookies and Headers Parameters
@app.post(
    path = "/contact",
    status_code = status.HTTP_200_OK
)
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length=20,
    ),
    user_agent: Optional[str] = Header(default = None),
    ads: Optional[str] = Cookie(default=None)
    ):
    return user_agent

@app.post(
    path = "/post-image",
    tags = ["Images"]
    )
def post_image(
    image: UploadFile = File(...)
    ):
    return {
        "Filename": image.filename, 
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024, ndigits=2)
    }

@app.post(
    path='/post-images',
    tags = ["Images"]
)
def post_images(
    images: List[UploadFile] = File(...)
):
    info_images = [{
        "filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024, ndigits=2)
    } for image in images]

    return info_images