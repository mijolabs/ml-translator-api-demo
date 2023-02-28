from typing import Union

from pydantic import BaseModel



class DetectionRequest(BaseModel):
    text: str

    class Config:
        schema_extra = {
            "example": {
                "text": "Привет, это хороший день."
            }
        }

class DetectionResult(BaseModel):
    language: str
    probability: float

    class Config:
        schema_extra = {
            "example": {
                "language": "ru",
                "probability": 0.9923186302185059
            }
        }

class ErrorResponse(BaseModel):
    error: str

class TranslationRequest(BaseModel):
    source: Union[str, None] = None
    target: Union[str, None] = "en"
    text: str

    class Config:
        schema_extra = {
            "example": {
                "source": "ru",
                "target": "en",
                "text": "Привет, это хороший день."
            }
        }

class TranslationResult(BaseModel):
    source: str
    target: str
    translation: str

    class Config:
        schema_extra = {
            "example": {
                "source": "ru",
                "target": "en",
                "translation": "Hey, it's a good day."
            }
        }
