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

# Support running as an arbitrary host UID/GID by making the working directory writable
COPY --from=builder /app/target/arsh-1.0-SNAPSHOT.jar app.jar
RUN chmod 777 /app

# Setting sensible JVM resource limits for a Discord bot
ENTRYPOINT ["java", "-XX:+UseZGC", "-Xmx512m", "-Xms256m", "-jar", "app.jar"]
