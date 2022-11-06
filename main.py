#Python
from typing import Optional
from enum import Enum
import re
from datetime import date
from typing import Dict
from typing import Any

#Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr
from pydantic import PaymentCardNumber
from pydantic.validators import str_validator
from pydantic.types import PaymentCardBrand

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

PHONE_REGEXP = re.compile(r'^\+?[0-9]{1,3}?[0-9]{6,14}$')

# Models

class PhoneNumber(str):
    """Phone number type"""

    @classmethod
    def __get_validators__(cls) -> Dict[str, Any]:
        yield str_validator
        yield cls.validate

    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        field_schema.update(
            pattern=r'^\+?[0-9]+$',
            example=['+541112345678'],
            format='phone-number',
        )

    @classmethod
    def validate(cls, value: str) -> str:
        if not isinstance(value, str):
            raise TypeError('Phone number must be a string')

        match = PHONE_REGEXP.search(value)

        if not match:
            raise ValueError('Phone number must be a valid phone number')

        return value

    def __repr__(self) -> str:
        return f'PhoneNumber({super().__repr__()})'

    
class HairColor(str, Enum):
    white = "white",
    brown = "brown",
    black = "black", 
    blonde = "blonde",
    red = "red"

class Person(BaseModel):
    first_name: str = Field(
        ..., 
        min_length=1,
        max_length = 50,
        )
    last_name: str = Field(
        ..., 
        min_length=1,
        max_length = 50
        )
    age: int = Field(
        ..., 
        gt = 0,
        le = 115
        )
    hair_color: Optional[HairColor] = Field(default = None)
    is_married : Optional[bool] =  Field(default = None)

    class Config:
        schema_extra = {
            "example":{
                "first_name": "Facundo",
                "last_name" : "García Martoni",
                "age": 21,
                "hair_color": "blonde",
                "is_married": False
            }
        }

class Location(BaseModel):
    city: str
    state: str
    country: str

@app.get("/") #Fast operation decorator
def home():
    
    return {"Hello": "world"}

#Request an Response body

@app.post("/person/new") # Enviar datos
def create_person(person: Person = Body(...)): #El body parameter es obligatorio

    return person

# Validaciones: Query Parameters
@app.get("/person/detail")
def show_person( #recibo query parameters
    name: Optional[str] = Query(
        None, 
        min_length = 1, 
        max_length = 20,
        title = "Person Name", 
        description = "This is the person's mame. It's between 1 and 20 characters"
        ),
    age: Optional[int] = Query(
        ...,
        title = "Person Age", 
        description = "This is the person's age. It's rquired"
        ) #Query parameter obligatorio, no es ideal pero puede pasar
    ):
    return {name: age}

# Validaciones: Path parameters
@app.get("/person/detail/{person_id}")
def show_person( #recibo path parameters
    person_id: int = Path(
        ..., 
        gt = 0,
        title = "Person Id", 
        description = "This is the person's Id. It's rquired and it must be greather than 0"
        ) # Obligatorio y mayor a 0
    ):
    return {person_id: "It exists!"}

# Validaciones: Request Body

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ..., 
        gt = 0,
        title = "Person ID",
        description= "This is the person ID"
    ),
        person: Person = Body(...),
        # location: Location = Body(...)
):
    results = person.dict()
    # results.update(location.dict())
    # return {
    #     "person": person.dict(),
    #     "location": location.dict()
    # }
    return person