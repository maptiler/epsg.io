import pytest
from os import sys, path

@pytest.fixture
def client():
    sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
    from app import app

    app.testing = True
    client = app.test_client()
    return client