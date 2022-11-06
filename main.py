#Python
from typing import Optional

#Pydantic
from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query

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
def show_person(
    name: Optional[str] = Query(None, min_length = 1, max_length = 20),
    age: Optional[int] = Query(...) #Query parameter obligatorio, no es ideal pero puede pasar
):
    return {name: age}
