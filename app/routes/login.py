# app.py
from flask import Flask, request, jsonify
import bcrypt, jwt, os
from supabase import create_client

app = Flask(__name__)

supabase = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_SERVICE_ROLE_KEY"]
)

JWT_SECRET = os.environ["JWT_SECRET"]

@app.post("/api/login")
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    res = supabase.table("admin_users") \
        .select("*") \
        .eq("username", username) \
        .eq("is_active", True) \
        .execute()

    if not res.data:
        return jsonify({"error": "Invalid credentials"}), 401

    user = res.data[0]

    if not bcrypt.checkpw(
        password.encode(),
        user["password_hash"].encode()
    ):
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode(
        {"user_id": user["id"], "role": user["role"]},
        JWT_SECRET,
        algorithm="HS256"
    )

    return jsonify({"token": token})
