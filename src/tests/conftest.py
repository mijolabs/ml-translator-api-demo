from fastapi.testclient import TestClient
from pytest import fixture

from app.main import app
from app.polyglot import Polyglot



@fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client


@fixture(scope="module")
def polyglot():
    return Polyglot()
