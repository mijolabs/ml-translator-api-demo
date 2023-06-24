from fastapi.testclient import TestClient
from pytest import fixture

from app.main import app
from app.translator import Translator



@fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client


@fixture(scope="module")
def translator():
    return Translator()
