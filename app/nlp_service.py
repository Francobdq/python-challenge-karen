from pandasai import Agent
import os
from fastapi import APIRouter, Request
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

@nlp_endpoint.post("/")
async def nlp_post(request: Request, body: NLPQuery):
    result = nlp(body.question)
    return {
        "question": body.question,
        "answer": result
    }
