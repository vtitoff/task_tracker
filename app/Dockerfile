FROM python:3.12-slim

WORKDIR /opt/app/

COPY . .


RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi --no-root


ENTRYPOINT ["sh", "./entrypoint.sh"]
