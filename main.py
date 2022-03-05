from fastapi import FastAPI, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from database import Database
from typing import Tuple

app = FastAPI()
app.db = Database()


class AlphaRange(BaseModel):
    alphas: Tuple[float, float, float]


@app.get('/')
def get_alpha(alpha: float):
    return app.db.get(alpha)


@app.post('/')
def post_range(rng: AlphaRange):
    app.db.put(rng)
    return app.db.get(rng)


@app.delete('/')
def delete_all():
    return app.db.delete_all()
