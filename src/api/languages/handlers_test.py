from http import HTTPStatus

from pytest import mark


@mark.parametrize(
    "input_text",
    [
        ("Привет, это хороший день."),
        ("你好，这是美好的一天。"),
    ],
    ids=["ru", "zh"],
)
def test_v1_detect(client, input_text):
    endpoint = "/v1/detect"

    json_data = {"text": input_text}

    response = client.post(endpoint, json=json_data)

    assert response.status_code == HTTPStatus.OK
    assert {"language", "probability"} <= response.json().keys()
    assert "x-process-duration" in response.headers


@mark.parametrize(
    "input_text, source_language, http_status, response_keys",
    [
        ("Привет, это хороший день.", "ru", HTTPStatus.OK, {"source", "target", "translation"}),
        ("你好，这是美好的一天。", "zh", HTTPStatus.OK, {"source", "target", "translation"}),
        ("Привет, это хороший день.", None, HTTPStatus.OK, {"source", "target", "translation"}),
        ("Detta är svenska", "se", HTTPStatus.BAD_REQUEST, {"detail"}),
    ],
    ids=[
        "ru-en",
        "zh-en",
        "Source language auto-detection",
        "Invalid language pair: se-en",
    ],
)
def test_v1_translate(client, input_text, source_language, http_status, response_keys):
    endpoint = "/v1/translate"

    json_data = {"source": source_language, "text": input_text}

    response = client.post(endpoint, json=json_data)

    assert response.status_code == http_status
    assert response_keys <= response.json().keys()
    assert "x-process-duration" in response.headers
