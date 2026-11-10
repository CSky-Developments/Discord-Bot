FROM eclipse-temurin:21-jdk AS jdk

FROM python:3.12-slim-bookworm

# Copy OpenJDK 21 from eclipse-temurin for runtime Spigot plugin builds
COPY --from=jdk /opt/java/openjdk /opt/java/openjdk
ENV JAVA_HOME=/opt/java/openjdk \
    PATH="/opt/java/openjdk/bin:${PATH}" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TMPDIR=/tmp \
    HOME=/tmp

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot/ ./bot/
COPY src/main/resources/config.yml ./config.yml

CMD ["python", "-m", "bot.main"]
