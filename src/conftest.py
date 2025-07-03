from collections.abc import AsyncGenerator, Callable
from contextlib import contextmanager
from typing import Any

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient


@pytest.fixture()
def app() -> FastAPI:
    from main import app

    return app


@pytest.fixture()
async def test_client(app) -> AsyncGenerator[AsyncClient]:
    _base_url = "http://test"
    async with AsyncClient(transport=ASGITransport(app=app), base_url=_base_url) as client:
        yield client


@pytest.fixture()
def override_dependency(app) -> Callable:
    @contextmanager
    def _override(dependency: Callable, return_value: Any) -> Any:
        app.dependency_overrides[dependency] = lambda: return_value
        try:
            yield
        finally:
            app.dependency_overrides = {}

    return _override
