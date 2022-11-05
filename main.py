from fastapi import FastAPI

app = FastAPI()

@app.get("/") #Fast operation decorator
def home():
    
    return {"Hello": "world"}