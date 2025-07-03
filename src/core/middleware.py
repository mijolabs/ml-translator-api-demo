from collections.abc import Callable
from timeit import default_timer as timestamp

from fastapi import Request, Response


def register_middleware(app) -> None:
    @app.middleware("http")
    async def add_process_duration_header(request: Request, call_next: Callable) -> Response:
        start_time: float = timestamp()
        response: Response = await call_next(request)
        process_time: str = f"{(timestamp() - start_time):.4f}"
        response.headers["X-Process-Duration"] = str(process_time)

        return response
