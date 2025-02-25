from fastapi import FastAPI
from agent import get_motivation

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Study Motivator API is running!"}

@app.get("/motivate")
def motivate(prompt: str):
    response = get_motivation(prompt)
    return {"response": response}