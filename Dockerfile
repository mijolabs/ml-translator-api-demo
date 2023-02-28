# https://testdriven.io/blog/fastapi-crud/

FROM python:3.9.13-slim
# Upgrade project to 3.11 when PyTorch has a build for it

WORKDIR /polyglot-api

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./pretrained /polyglot-api/pretrained
COPY ./src /polyglot-api/src

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
