from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.languages.handlers import router as languages_router
from core.lifespan import enter_lifespan


app = FastAPI(
    title="ML Translator API Demo",
    version="0.1.0",
    description="An API for language detection and translation using machine learning models.",
    lifespan=enter_lifespan,
    default_response_class=ORJSONResponse,
)


@app.get("/health", tags=["Health"])
async def handle_health_check() -> dict:
    return {}


app.include_router(languages_router)


if __name__ == "__main__":
    import uvicorn

    # app_dir = str(Path(__file__).parent.parent)

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=80,
        workers=1,
        # app_dir=app_dir,
        reload=True,
        # reload_dirs=app_dir,
        reload_includes=["*.yml"],
    )
