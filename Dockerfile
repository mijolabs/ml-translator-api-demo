FROM python:3.13-slim AS builder

ENV UV_LINK_MODE=copy \
  UV_PYTHON_DOWNLOADS=0 \
  UV_LOCKED=1 \
  UV_COMPILE_BYTECODE=1 

COPY --link --from=ghcr.io/astral-sh/uv:latest /uv /bin/

RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  --mount=type=secret,id=ACCESS_TOKEN \
  export PATH=$(uv tool dir --bin):$PATH && \
  apt update && apt install -y --no-install-recommends build-essential cmake && \
  uv sync --no-dev && \
  uv run python -c "import nltk; nltk.download('punkt')"

# ENTRYPOINT ["/bin/bash"]


FROM python:3.13-slim AS final

ENV PYTHONUNBUFFERED=1 \
  PORT=8080

RUN groupadd --system app && useradd --system --no-create-home --gid app app

USER app
WORKDIR /app
EXPOSE ${PORT}

COPY --from=builder --chown=app:app .venv .venv
COPY --chown=app:app src/ .

ENTRYPOINT [".venv/bin/python", "main.py"]


# # //////////////////
# FROM python:3.10.9-slim

# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1
# ENV NLTK_DATA ~/nltk_data

# WORKDIR /translator-api

# COPY ./requirements.txt .
# COPY ./pretrained-models ./pretrained-models

# RUN pip install --upgrade pip \
#   && pip install --no-cache-dir --upgrade -r requirements.txt \
#   && python -c "import nltk;nltk.download('punkt')" \
#   && rm ~/nltk_data/tokenizers/punkt.zip \
#   && rm ~/nltk_data/tokenizers/punkt/*.pickle \
#   && rm ~/nltk_data/tokenizers/punkt/README

# COPY ./app ./app

# EXPOSE 80

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
