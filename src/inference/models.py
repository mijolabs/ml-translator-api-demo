from pydantic import BaseModel, ConfigDict


class DetectionResult(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"language": "ru", "probability": 0.9923186302185059},
            ],
        },
    )

    language: str
    probability: float


class TranslationResult(BaseModel):
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
