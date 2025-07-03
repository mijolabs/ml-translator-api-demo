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
  uv run python -c "import nltk;nltk.download('punkt_tab', download_dir='.venv/nltk_data')" && \
  rm .venv/nltk_data/tokenizers/punkt_tab.zip .venv/nltk_data/tokenizers/punkt_tab/README


FROM python:3.13-slim AS final

ENV PORT=8080 \
  PYTHONUNBUFFERED=1

RUN groupadd --system app && useradd --system --no-create-home --gid app app

USER app
WORKDIR /app
EXPOSE ${PORT}

COPY --from=builder --chown=app:app .venv .venv
COPY --chown=app:app src/ .

ENTRYPOINT [".venv/bin/python", "main.py"]
