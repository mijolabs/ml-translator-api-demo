from http import HTTPStatus
from unittest.mock import MagicMock, patch

import httpx

from dependencies.context import get_context


@patch("api.languages.handlers.detect_language")
async def test_detection_handler(
    mock_detect_language,
    override_dependency,
    test_client,
) -> None:
    mock_context = MagicMock()
    json_data: dict = {"text": "Привет, это хороший день."}
    mock_detect_language.return_value = MagicMock(language="ru", probability=0.99)

    with override_dependency(get_context, mock_context):
        r: httpx.Response = await test_client.post("/languages/detection", json=json_data)

    mock_detect_language.assert_called_once_with(context=mock_context, text=json_data["text"])
    assert r.status_code == HTTPStatus.OK
    assert set(r.json().keys()) == {"language", "probability"}


@patch("api.languages.handlers.detect_language")
@patch("api.languages.handlers.translate_text")
async def test_translation_handler(
    mock_translate_text,
    mock_detect_language,
    override_dependency,
    test_client,
) -> None:
    mock_context = MagicMock()
    json_data: dict = {"source": "zh", "target": "en", "text": "你好，这是美好的一天。"}
    expected_response: dict = {
        "source": "zh",
        "target": "en",
        "result": "Hello, it's a beautiful day.",
    }
    mock_translate_text.return_value = MagicMock(**expected_response)

    with override_dependency(get_context, mock_context):
        r: httpx.Response = await test_client.post("/languages/translation", json=json_data)

    mock_detect_language.assert_not_called()
    mock_translate_text.assert_called_once_with(
        context=mock_context,
        source=json_data["source"],
        target=json_data["target"],
        text=json_data["text"],
    )
    assert r.status_code == HTTPStatus.OK
    assert r.json() == expected_response


@patch("api.languages.handlers.detect_language")
@patch("api.languages.handlers.translate_text")
async def test_translation_handler_without_languages_provided(
    mock_translate_text,
    mock_detect_language,
    override_dependency,
    test_client,
) -> None:
    mock_context = MagicMock()
    json_data: dict = {"text": "你好，这是美好的一天。"}
    expected_response: dict = {
        "source": "zh",
        "target": "en",
        "result": "Hello, it's a beautiful day.",
    }
    mock_translate_text.return_value = MagicMock(**expected_response)

    with override_dependency(get_context, mock_context):
        r: httpx.Response = await test_client.post("/languages/translation", json=json_data)

    mock_detect_language.assert_called_once_with(context=mock_context, text=json_data["text"])
    mock_translate_text.assert_called_once_with(
        context=mock_context,
        source=mock_detect_language.return_value.language,
        target="en",
        text=json_data["text"],
    )
    assert r.status_code == HTTPStatus.OK
    assert r.json() == expected_response
