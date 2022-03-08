from fastapi import FastAPI
from pydantic import BaseModel
from database import Database
from typing import Tuple

app = FastAPI()
app.db = Database()


class AlphaRange(BaseModel):
    alphas: Tuple[float, float, float]


@app.get('/')
def homepage():
    return {'Sklearn alpha penalty demonstration': "Synchronous vs Multiprocessing speed comparison"}


@app.get('/{vals}')
def get_alpha_range(vals: str) -> str:
    vals = tuple(float(v) for v in vals.split('_'))
    rng = AlphaRange(alphas=vals)
    return str(app.db.get(rng))


@app.post('/sync')
def post_range_sync(rng: AlphaRange) -> str:
    app.db.put_sync(rng)
    return str(app.db.get(rng))


@app.post('/mp')
def post_range_mp(rng: AlphaRange) -> str:
    app.db.put_mp(rng)
    return str(app.db.get(rng))


@app.delete('/')
def delete_all():
    return app.db.delete_all()
