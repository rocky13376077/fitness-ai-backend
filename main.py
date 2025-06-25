from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import openai
import os
from dotenv import load_dotenv
from fastapi import Header, HTTPException

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
def generate_plan(
    data: PlanRequest,
    api_key: str = Header(None)
):
    if api_key != os.getenv("API_SECRET"):
        raise HTTPException(status_code=401, detail="Unauthorized")

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

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Du bist ein professioneller Ernährungs- und Fitnesstrainer."},
            {"role": "user", "content": prompt}
        ]
    )

    return PlanResponse(plan=response.choices[0].message.content.strip())


    
