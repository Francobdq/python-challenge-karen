from fastapi import FastAPI
from app.graphql_service import graphql_endpoint
from app.nlp_service import nlp_endpoint

app = FastAPI()

app.include_router(graphql_endpoint, prefix="/graphql")
app.include_router(nlp_endpoint, prefix="/nlp")

@app.get("/")
async def root():
    return {"message": "API root, revisa /docs para acceder a la documentación."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
