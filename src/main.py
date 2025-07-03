from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.languages.handlers import router as languages_router
from core.exceptions import register_exception_handlers
from core.health import register_health_endpoint
from core.lifespan import enter_lifespan
from core.middleware import register_middleware
from core.openapi import set_custom_openapi


UVICORN_DEFAULT_PORT: int = 8080


app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=enter_lifespan,
)

set_custom_openapi(app)
register_middleware(app)
register_exception_handlers(app)
register_health_endpoint(app)

app.include_router(languages_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=UVICORN_DEFAULT_PORT,
        workers=1,
    )
