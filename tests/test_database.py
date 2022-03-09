from database import Database
import pytest


@pytest.fixture
def db():
    dab = Database()