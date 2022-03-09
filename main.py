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
    """
    split the input into start, stop, step floats
    :param vals: input string
    :return: the model results in str
    """
    vals = tuple(float(v) for v in vals.split('_'))
    rng = AlphaRange(alphas=vals)
    return str(app.db.get(rng))


@app.post('/sync')
def post_range_sync(rng: AlphaRange) -> str:
    """
    post penalties and model results into DB and return what was posted
    :param rng: penalty range
    :return: string of model results posted
    """
    app.db.put_sync(rng)
    return str(app.db.get(rng))


@app.post('/mp')
def post_range_mp(rng: AlphaRange) -> str:
    """
    same as `post_range_sync` except using multiprocessing
    :param rng: penalty range
    :return: string of model results posted
    """
    app.db.put_mp(rng)
    return str(app.db.get(rng))


@app.delete('/')
def delete_all():
    """
    set DB to empty
    :return: boolean for True if something was in DB before deletion and False if empty
    """
    return app.db.delete_all()
