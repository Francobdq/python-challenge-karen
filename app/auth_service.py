import os
import jwt
import datetime
from functools import wraps
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

SECRET_KEY = os.urandom(24).hex()
ALGORITHM = "HS256"

auth_endpoint = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# usuario de prueba (en un entorno real, esto se haría en una base de datos)
fake_user_db = {
    "user": {
        "username": "user",
        "password": "password",
        "role": "admin"
    }
}

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str

@auth_endpoint.post('/login', response_model=TokenResponse, summary="Iniciar sesión", description="Autentica a un usuario y devuelve un token de acceso.")
async def login(login_data: LoginRequest):
    user = fake_user_db.get(login_data.username)
    if not user or user["password"] != login_data.password:
        raise HTTPException(status_code=401, detail="Bad username or password")

    access_token = jwt.encode(
        {"sub": login_data.username, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return {"access_token": access_token}


def jwt_required(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
        request: Request = kwargs.get('request')
        token = kwargs.get('token')
        if not token:
            raise HTTPException(status_code=401, detail="Authorization header missing")

        try:
            jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

        return await f(*args, **kwargs)
    return decorated
