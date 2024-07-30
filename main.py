# main.py
from fastapi import FastAPI
from app.graphql_service import graphql_endpoint
from app.nlp_service import nlp_endpoint
from app.auth_service import auth_endpoint

app = FastAPI(
    title="API Personalizada",
    description="Esta es una API personalizada utilizando FastAPI para proporcionar servicios de autenticación, procesamiento de lenguaje natural y GraphQL.",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "auth",
            "description": "Operaciones relacionadas con la autenticación de usuarios."
        },
        {
            "name": "graphql",
            "description": "Operaciones relacionadas con el servicio GraphQL."
        },
        {
            "name": "nlp",
            "description": "Operaciones relacionadas con el procesamiento de lenguaje natural (NLP)."
        }
    ]
)

app.include_router(graphql_endpoint, prefix="/graphql", tags=["graphql"])
app.include_router(nlp_endpoint, prefix="/nlp", tags=["nlp"])
app.include_router(auth_endpoint, prefix="/auth", tags=["auth"])

@app.get("/", summary="Root endpoint", description="Endpoint raíz que proporciona un mensaje de bienvenida y dirección a la documentación.")
async def root():
    return {"message": "API root, revisa /docs para acceder a la documentación."}

# documentacion Swagger se genera automaticamente por FastAPI en /docs

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
