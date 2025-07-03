from unittest.mock import MagicMock

import pytest

from inference.detection import (
    MIN_PROBABILITY,
    LanguageDetectionError,
    detect_language,
)


def test_detect_language() -> None:
    mock_context = MagicMock()
    sample_text = "Привет, это\r\nхороший\nдень."
    mock_predict = MagicMock()
    mock_predict.return_value = (["__label__ru"], [0.9923186302185059])
    mock_context.inference.fasttext.predict = mock_predict

    detect_language(context=mock_context, text=sample_text)

    mock_predict.assert_called_once_with(
        text="Привет, это хороший день.",
        threshold=MIN_PROBABILITY,
    )


def test_detect_language_raises_on_failed_detection() -> None:
    mock_context = MagicMock()
    sample_text = "Привет, это\r\nхороший\nдень."
    mock_predict = MagicMock()
    mock_predict.return_value = ([], [])
    mock_context.inference.fasttext.predict = mock_predict

    with pytest.raises(LanguageDetectionError):
        detect_language(context=mock_context, text=sample_text)

    mock_predict.assert_called_once_with(
        text="Привет, это хороший день.",
        threshold=MIN_PROBABILITY,
    )
