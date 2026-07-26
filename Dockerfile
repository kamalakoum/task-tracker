FROM python:3.11-slim AS builder

WORKDIR /build

COPY requirements.txt .

RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install -r requirements.txt


FROM python:3.11-slim

WORKDIR /app

RUN useradd -m -u 1000 app

COPY --from=builder /opt/venv /opt/venv
COPY app/ ./app/

RUN chown -R app:app /app

ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 8000

USER app

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import http.client; conn = http.client.HTTPConnection('127.0.0.1', 8000); conn.request('GET', '/health'); exit(0 if conn.getresponse().status == 200 else 1)"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
