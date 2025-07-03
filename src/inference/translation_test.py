from unittest.mock import MagicMock, patch

import pytest

from inference.translation import UnsupportedLanguagePairError, translate_text


@patch("inference.translation.generate_translation")
def test_translate_text(mock_generate_translation) -> None:
    mock_context = MagicMock()
    sample_source = "ru"
    sample_target = "en"
    sample_text = "Привет, мир!"

    translate_text(
        context=mock_context,
        source=sample_source,
        target=sample_target,
        text=sample_text,
    )

    mock_generate_translation.assert_called_once_with(
        context=mock_context,
        source=sample_source,
        target=sample_target,
        text=sample_text,
    )


@patch("inference.translation.generate_translation")
def test_translate_text_unsupported_language_pair(mock_generate_translation) -> None:
    sample_source = "xx"
    sample_target = "en"

    with pytest.raises(UnsupportedLanguagePairError):
        translate_text(
            context=MagicMock(),
            source=sample_source,
            target=sample_target,
            text=MagicMock(),
        )

    mock_generate_translation.assert_not_called()
