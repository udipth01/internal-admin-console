from fastapi import APIRouter, Form, HTTPException
from app.db import supabase
from app.auth import verify_password, create_token

router = APIRouter()

@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    res = supabase.table("admin_users").select("*").eq("username", username).execute()
    if not res.data:
        raise HTTPException(401, "Invalid credentials")

    user = res.data[0]
    if not verify_password(password, user["password_hash"]):
        raise HTTPException(401, "Invalid credentials")

    token = create_token({"user_id": user["id"], "role": user["role"]})
    return {"access_token": token}
