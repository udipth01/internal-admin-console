# app/routes/login.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import bcrypt, jwt, os

from app.supabase_client import supabase

router = APIRouter()

JWT_SECRET = os.environ["JWT_SECRET"]

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/api/login")
def login(data: LoginRequest):
    res = supabase.table("admin_users") \
        .select("*") \
        .eq("username", data.username) \
        .eq("is_active", True) \
        .execute()

    if not res.data:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user = res.data[0]

    if not bcrypt.checkpw(
        data.password.encode(),
        user["password_hash"].encode()
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode(
        {"user_id": user["id"], "role": user["role"]},
        JWT_SECRET,
        algorithm="HS256"
    )

    return {"token": token}
