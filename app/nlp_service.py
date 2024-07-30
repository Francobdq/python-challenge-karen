from pandasai import Agent
import os
from fastapi import APIRouter, Request, Depends
from app.auth_service import jwt_required, oauth2_scheme 
from pydantic import BaseModel
import pandas as pd

from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("PANDASAI_API_KEY")

nlp_endpoint = APIRouter()

data_path = 'data/data.csv'
df = pd.read_csv(data_path)

os.environ["PANDASAI_API_KEY"] = API_KEY

def nlp(question):
    agent = Agent(df)
    response = agent.chat(question)
    return response

class NLPQuery(BaseModel):
    question: str

class NLPResponse(BaseModel):
    question: str
    answer: str

@nlp_endpoint.post(
    "/",
    summary="Procesar consulta NLP",
    description="Procesa una consulta de lenguaje natural y devuelve la respuesta.",
    response_model=NLPResponse,
    responses={
        200: {
            "description": "Respuesta exitosa",
            "content": {
                "application/json": {
                    "example": {
                        "question": "La pregunta al modelo npl",
                        "answer": "La respuesta del modelo"
                    }
                }
            }
        }
    }
)
@jwt_required
async def nlp_post(request: Request, body: NLPQuery, token: str = Depends(oauth2_scheme)):
    result = nlp(body.question)
    return {
        "question": body.question,
        "answer": result
    }
