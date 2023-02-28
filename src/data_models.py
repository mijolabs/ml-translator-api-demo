from typing import Union

from pydantic import BaseModel



class DetectionRequest(BaseModel):
    text: str

class DetectionResult(BaseModel):
    language: str
    probability: float

class ErrorResponse(BaseModel):
    error: str

class TranslationRequest(BaseModel):
    source: Union[str, None] = None
    target: Union[str, None] = "en"
    text: str

class TranslationResult(BaseModel):
    source: str
    target: str
    translation: str
