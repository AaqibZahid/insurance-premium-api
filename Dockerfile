# syntax=docker/dockerfile:1

FROM python:3.13-slim

# metadata
LABEL maintainer="AaqibZahid"
LABEL description="Insurance Premium Prediction API (FastAPI + scikit-learn)"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# install dependencies first so this layer is cached between builds
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy application code
COPY app.py .
COPY config/ config/
COPY model/ model/
COPY schema/ schema/

# run as non-root user
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
