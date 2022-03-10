from fastapi import FastAPI, HTTPException, responses
from pydantic import BaseModel
from database import Database
from typing import Tuple

app = FastAPI()
app.db = Database()


class AlphaRange(BaseModel):
    """
    stores penalty generator parameters
    whether multiprocess or not
    """
    alphas: Tuple[float, float, float]
    mp: bool


@app.get('/')
def homepage():
    return {'Sklearn alpha penalty demonstration': "Synchronous vs Multiprocessing speed comparison"}


@app.get('/{vals}')
def get_alpha_range(vals) -> str:
    """
    split the input into start, stop, step floats
    :param vals: input alpha params
    :return: the model results in str
    """
    rng = rng_parse(vals)
    res = app.db.get(rng)
    if not res:
        raise HTTPException(status_code=404, detail=f"{vals} not found in database!")
    return res


@app.get('/{vals}/image', response_class=responses.Response)
def get_alpha_range_image(vals: str):
    """
    NOT IMPLEMENTED BECAUSE I COULDN'T GET MATPLOTLIB TO INSTALL ON VIRTUALENV
    :param vals:
    :return: plot of whatever
    """
    rng = rng_parse(vals)
    image_bytes = app.db.get_image(rng)
    return responses.Response(content=image_bytes, media_type='image/png')


@app.post('/')
def post_range(rng: AlphaRange) -> str:
    """
    post penalties and model results into DB and return what was posted
    :param rng: penalty range
    :return: string of model results posted
    """
    if not check_rng(rng.alphas):
        raise HTTPException(status_code=400, detail='Input values not acceptable')
    app.db.put_db(rng)
    return app.db.get(rng)


@app.delete('/')
def delete_all():
    """
    set DB to empty
    :return: boolean for True if something was in DB before deletion and False if empty
    """
    return app.db.delete_all()


def check_rng(rng: tuple) -> bool:
    """
    check valid inputs
    :param rng: alpha range
    :return: true for valid and false if not
    """
    if rng[1] <= rng[0]:
        return False
    if rng[2] > rng[1] - rng[0]:
        return False
    return True


def rng_parse(vals):
    """
    parse the get app parameter, otherwise raise HTTPException
    :param vals: the input values in #_#_# format where # is a float
    :param mp: multiprocessing bool
    :return: tuple of (start, stop, step) in float
    """
    try:
        splits = vals.split('_')
        mp_bool = bool(int(splits[-1]))
        vals_t = tuple(float(v) for v in splits[:-1])
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Input {vals} are invalid")
    rng = AlphaRange(alphas=vals_t, mp=mp_bool)
    return rng
