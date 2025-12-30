# app/main.py
from fastapi import FastAPI
from app.routes import login, tables

app = FastAPI()

app.include_router(login.router)
app.include_router(tables.router)
