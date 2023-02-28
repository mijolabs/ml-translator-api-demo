from pytest import fixture

from src.polyglot import Polyglot



@fixture(scope="module")
def polyglot():
    return Polyglot()
