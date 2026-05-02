FROM python:3.14-slim AS builder

WORKDIR /app
RUN pip install uv
COPY pyproject.toml .
RUN uv pip install --system --no-cache-dir .

FROM python:3.14-slim AS runtime

WORKDIR /app
COPY --from=builder /usr/local/lib/python3.14 /usr/local/lib/python3.14
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn
COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:application", "--host", "0.0.0.0", "--port", "8000"]
