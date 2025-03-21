FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY src/requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY src/ /app/

EXPOSE 8000

COPY deploy/prod/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "algopath.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]