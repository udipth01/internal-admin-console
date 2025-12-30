# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import login, tables

app = FastAPI()

# 🔥 THIS IS MISSING 🔥
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(login.router)
app.include_router(tables.router)
