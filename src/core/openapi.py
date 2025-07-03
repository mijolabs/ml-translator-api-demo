from fastapi.openapi.utils import get_openapi


def set_custom_openapi(app) -> None:
    def custom_openapi() -> dict:
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema: dict = get_openapi(
            title="ml-translator-api-demo",
            version="0.1.0",
            description=(
                "A proof-of-concept API for language detection and translation using machine learning models."
            ),
            routes=app.routes,
        )

        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi
