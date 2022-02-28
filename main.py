from fastapi import FastAPI, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from database import Database


app = FastAPI()
app.db = Database()


@app.get('/')
def home():
    return {}


@app.get('/{alpha}')
def get_alpha(alpha: float):
    return app.db.get(alpha)


@app.post('/{alpha}')
def create_distribution(alpha: float):
    app.db.put(alpha)
    return app.db.get(alpha)


@app.delete('/')
def delete_distribution(alpha: float):
    return app.db.delete(alpha)