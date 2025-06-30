from app.schemas import DetectionRequest, DetectionResult, TranslationRequest, TranslationResult


def test_detect_language(translator):
    detection_request = DetectionRequest(text="Привет, это хороший день.")
    result = translator.detect_language(detection_request)

    assert isinstance(result, DetectionResult)
    assert isinstance(result.language, str)
    assert isinstance(result.probability, float)


def test_generate_translation(translator):
    translation_request = TranslationRequest(source="ru", text="Привет, это хороший день.")
    result = translator.generate_translation(translation_request)

    assert isinstance(result, TranslationResult)
    assert isinstance(result.translation, str)
    assert result.source == "ru"
    assert result.target == "en"
