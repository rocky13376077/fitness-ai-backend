from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import openai
import os
from dotenv import load_dotenv

# Lade Umgebungsvariablen
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class PlanRequest(BaseModel):
    age: int
    gender: str
    height: float
    weight: float
    goal: str
    activity_level: str
    diet: str = "Keine"
    allergies: str = "Keine"
    training_days: int

class PlanResponse(BaseModel):
    plan: str

@app.post("/generate_plan", response_model=PlanResponse)
def generate_plan(data: PlanRequest):
    prompt = f"""
    Erstelle einen 7-tägigen Ernährungs- und Fitnessplan für folgende Person:
    Alter: {data.age}, Geschlecht: {data.gender}
    Größe: {data.height} cm, Gewicht: {data.weight} kg
    Ziel: {data.goal}
    Aktivitätslevel: {data.activity_level}
    Ernährung: {data.diet}
    Allergien: {data.allergies}
    Trainingshäufigkeit: {data.training_days}x pro Woche
    """
    
