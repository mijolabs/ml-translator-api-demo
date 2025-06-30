from app.main import app
from app.translator import Translator
from fastapi.testclient import TestClient
from pytest import fixture


@fixture()
def test_client():
    with TestClient(app) as test_client:
        yield test_client


@fixture(scope="module")
def translator():
    return Translator()
