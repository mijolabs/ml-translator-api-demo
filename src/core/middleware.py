from collections.abc import Callable
from timeit import default_timer as timestamp

from fastapi import Request, Response


async def add_process_duration_header(request: Request, call_next: Callable) -> Response:
    start_time = timestamp()
    response = await call_next(request)
    process_time = f"{(timestamp() - start_time):.4f}"
    response.headers["X-Process-Duration"] = str(process_time)

    return response
