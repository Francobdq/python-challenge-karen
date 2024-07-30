# Python Coding Challenge

## Requisitos

- Docker
- Docker Compose

## Cómo correr el proyecto

1. Clonar el repositorio
2. Navegar al directorio del proyecto
3. Ejecutar `docker-compose up web`

La API estará disponible en `http://localhost:8000`.


## Cómo ejecutar los tests

1. Asegurarse de tener la aplicación ya clonada
2. Ejecutar `docker-compose run --rm tests`

## Endpoints

- `/graphql`: Endpoint GraphQL
- `/nlp`: Endpoint NLP
- `/auth/login`: Endpoint de Auth
- `/docs`: Documentación Swagger

## Ejemplos 

- Obtener token de login:
```
curl -X POST http://localhost:8000/auth/login \
     -H "Content-Type: application/json" \
     -d '{
           "username": "user",
           "password": "password"
         }'
```

-  interactuar con NLP:
```
curl -L -X POST http://localhost:8000/nlp \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <token>" \
     -d '{
           "question": "give me a random id_tie_fecha_valor"
         }'
```

- interactuar con GraphQL:

```
curl -L -X POST http://localhost:8000/graphql \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <token>" \
     -d '{
           "query": "{ item(idGaProducto: \"-3637462437398938388\") { descGaSkuProducto } }"
         }'

```
