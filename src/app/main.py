from os import getenv
from timeit import default_timer as timestamp
from typing import Callable

from fastapi import FastAPI, Request, Response

from app.config import CONFIG
from app.routes import v1
from app.schemas import HealthCheckResult



config = CONFIG.api

app = FastAPI(
    title=config.title,
    version=config.version,
    description=config.description,
    docs_url=config.endpoints.docs.openapi,
    redoc_url=config.endpoints.docs.redoc,
)


if config.response.headers.process_duration:
    @app.middleware("http")
    async def add_process_duration_header(request: Request, call_next: Callable) -> Response:
        start_time = timestamp()
        response = await call_next(request)
        process_time = f"{(timestamp() - start_time):.4f}"
        response.headers["X-Process-Duration"] = str(process_time)

        return response


if healthcheck_endpoint := config.endpoints.healthcheck:
    @app.get(healthcheck_endpoint, tags=["Health"])
    async def _health() -> HealthCheckResult:
        return HealthCheckResult()


app.include_router(v1.router, prefix="/v1", tags=["v1"])
