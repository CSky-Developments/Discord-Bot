# Stage 1: Build the JAR
FROM maven:3.9.6-eclipse-temurin-21 AS builder
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline
COPY src ./src
RUN mvn clean package -DskipTests

# Stage 2: Run the Bot
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app

# Create non-root user for security
RUN addgroup -S botgroup && adduser -S botuser -G botgroup

COPY --from=builder --chown=botuser:botgroup /app/target/arsh-1.0-SNAPSHOT.jar app.jar
RUN chown -R botuser:botgroup /app

USER botuser

# Setting sensible JVM resource limits for a Discord bot
ENTRYPOINT ["java", "-XX:+UseZGC", "-Xmx512m", "-Xms256m", "-jar", "app.jar"]
