from typing import Union

from fastapi import APIRouter, HTTPException

from src.schemas import (
    DetectionRequest,
    DetectionResult,
    ErrorResponse,
    TranslationRequest,
    TranslationResult
)
from src.polyglot import Polyglot



router = APIRouter()
polyglot = Polyglot()


@router.post("/detect")
async def detect(detection_request: DetectionRequest) -> DetectionResult:
    return polyglot.detect_language(detection_request)


@router.post("/translate")
async def translate(translation_request: TranslationRequest) -> Union[TranslationResult, ErrorResponse]:
    return polyglot.translate(translation_request)
