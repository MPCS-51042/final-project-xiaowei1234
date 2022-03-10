from database import Database
from modelresults import ModelResults
import pytest
from run_models import lst_to_df
from fastapi.testclient import TestClient
from main import app
import matplotlib


client = TestClient(app)
dab = Database()
data = [[3, 2, 1], [3, 1, 2]]
model_results = ModelResults(lst_to_df(data), 1.0, False)
dab._data = {((1, 2, 1), False): model_results}
app.db = dab


@pytest.mark.parametrize(
    'payload, http_code',
    [
        ({'alphas': (1, 2, 0.5), 'mp': False}, 200),
        ({'alphas': (3, 1, 1), 'mp': True}, 400),
        ({'alphas': (1, 2, 2), 'mp': False}, 400),
    ]
)
def test_post(payload, http_code):
    response = client.post('/', json=payload)
    assert response.status_code == http_code


@pytest.mark.parametrize(
    'vals, status_code',
    [
        ('return error', 400),
        ('-1_2_0.1_a', 400),
        ('1_2_1_0', 200),
        ('1_2_1_1', 404),
    ]
)
def test_get(vals, status_code):
    response = client.get(f'/{vals}')
    assert response.status_code == status_code


def test_plot():
    fig = app.db.make_image(model_results)
    assert isinstance(fig, matplotlib.figure.Figure)
