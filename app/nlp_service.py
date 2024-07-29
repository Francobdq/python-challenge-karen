from fastapi import APIRouter, Request
import pandas as pd


nlp_endpoint = APIRouter()

data_path = 'data/data.csv'
df = pd.read_csv(data_path)


@nlp_endpoint.post("/")
async def nlp_post(request: Request):
    return {
        "question": "",
        "answer": ""
    }
