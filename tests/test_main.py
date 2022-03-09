from database import Database
from modelresults import ModelResults
import pytest
from run_models import lst_to_df
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)
dab = Database()
data = [[3, 2, 1], [3, 1, 2]]
model_results = ModelResults(lst_to_df(data), 1.0)
dab._data = {(1, 2, 1): model_results}
app.db = dab


@pytest.mark.parametrize(
    'payload, http_code',
    [
        ({'alphas': (1, 2, 0.5)}, 200),
        ({'alphas': (3, 1, 1)}, 400),
        ({'alphas': (1, 2, 2)}, 400),
    ]
)
@pytest.mark.parametrize(
    'url',
    ['sync', 'mp'],
)
def test_post(url, payload, http_code):
    response = client.post(f'/{url}', json=payload)
    assert response.status_code == http_code


@pytest.mark.parametrize(
    'vals, status_code',
    [
        ('return error', 400),
        ('-1_2_0.1', 404),
        ('1_2_1', 200),
    ]
)
def test_get(vals, status_code):
    response = client.get(f'/{vals}')
    assert response.status_code == status_code
