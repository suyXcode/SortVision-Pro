# SortVision Pro — production Docker image
FROM python:3.13-slim

WORKDIR /app

# System deps kept minimal; Flask + gunicorn need nothing beyond the base image.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Render/Railway inject $PORT; default to 8000 for local `docker run`.
ENV PORT=8000
ENV APP_CONFIG=production

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT} --workers 3 --threads 2 --timeout 60 app:app"]
