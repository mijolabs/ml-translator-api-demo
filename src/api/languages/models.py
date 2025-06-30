from pydantic import BaseModel, ConfigDict


class BaseRequestModel(BaseModel):
    model_config = ConfigDict(str_max_length=256)


class DetectionRequest(BaseRequestModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"text": "Привет, это хороший день."},
            ],
        },
    )

    text: str


class DetectionResult(BaseRequestModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"language": "ru", "probability": 0.9923186302185059},
            ],
        },
    )

    language: str
    probability: float


class TranslationRequest(BaseRequestModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"source": "ru", "target": "en", "text": "Привет, это хороший день."},
            ],
        },
    )

    source: str | None = None
    target: str = "en"
    text: str


class TranslationResult(BaseRequestModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"source": "ru", "target": "en", "result": "Hey, it's a good day."},
            ],
        },
    )

    source: str
    target: str
    result: str
