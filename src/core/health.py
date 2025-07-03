from fastapi import FastAPI


def register_health_endpoint(app: FastAPI) -> None:
    @app.get("/health", include_in_schema=False)
    async def handle_health_check() -> dict:
        return {}
