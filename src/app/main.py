from timeit import default_timer as timestamp
from typing import Callable

from fastapi import FastAPI, Request

from app.config import CONFIG
from app.routes import v1



config = CONFIG.api

app = FastAPI(
    title=config.title,
    version=config.version,
    description=config.description,
    docs_url=config.docs_endpoint.openapi,
    redoc_url=config.docs_endpoint.redoc,
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next: Callable):
    start_time = timestamp()
    response = await call_next(request)
    process_time = f"{(timestamp() - start_time):.3f}"
    response.headers["X-Process-Duration"] = str(process_time)

    return response


app.include_router(v1.router, prefix="/v1", tags=["v1"])
