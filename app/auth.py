import os
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.db import supabase

SECRET = os.getenv("JWT_SECRET", "change_me")
ALGO = "HS256"
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2 = OAuth2PasswordBearer(tokenUrl="/login")

def hash_password(pw):
    return pwd_ctx.hash(pw)

def verify_password(pw, hashed):
    return pwd_ctx.verify(pw, hashed)

def create_token(data: dict):
    data["exp"] = datetime.utcnow() + timedelta(hours=8)
    return jwt.encode(data, SECRET, algorithm=ALGO)

def get_current_user(token: str = Depends(oauth2)):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGO])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
