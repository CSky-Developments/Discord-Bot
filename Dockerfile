FROM python:3.12-slim-bookworm

# Install OpenJDK 21 headless for runtime plugin compilation via javac
RUN apt-get update && \
    apt-get install -y --no-install-recommends openjdk-21-jdk-headless ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TMPDIR=/tmp \
    HOME=/tmp

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot/ ./bot/
COPY src/main/resources/config.yml ./config.yml

CMD ["python", "-m", "bot.main"]
