FROM python:3.10.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV NLTK_DATA ~/nltk_data

WORKDIR /polyglot-api

COPY ./requirements.txt .
COPY ./pretrained-models ./pretrained-models

RUN pip install --upgrade pip \
  && pip install --no-cache-dir --upgrade -r requirements.txt \
  && python -c "import nltk;nltk.download('punkt')" \
  && rm ~/nltk_data/tokenizers/punkt.zip \
  && rm ~/nltk_data/tokenizers/punkt/*.pickle \
  && rm ~/nltk_data/tokenizers/punkt/README

COPY ./app ./app

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
