from fastapi import APIRouter, Request
import pandas as pd

graphql_endpoint = APIRouter()

data_path = 'data/data.csv'
df = pd.read_csv(data_path)


@graphql_endpoint.post("/")
async def graphql_post(request: Request):
    return {"message": "This is the GraphQL endpoint."}
    