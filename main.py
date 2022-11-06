#Python
from typing import Optional

#Pydantic
from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

# Models

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married : Optional[bool] = None


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