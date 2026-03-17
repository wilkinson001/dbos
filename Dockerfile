FROM python:3.14-slim

WORKDIR /app

ENV PYTHONPATH=.

COPY pyproject.toml .
COPY uv.lock .

RUN pip install --no-cache-dir uv==0.10.11 && uv pip install --system -r pyproject.toml

COPY src src
