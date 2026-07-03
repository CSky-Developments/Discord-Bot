# Deployment Guide

This document outlines the operational procedures for the CSky Developments Discord Bot.

## Overview
The bot is deployed using Docker and Docker Compose. We chose Docker to ensure the build environment (Maven) and runtime environment (Java 21) are consistent across all platforms and completely isolated.

## Runtime Requirements
- Docker and Docker Compose (V2 recommended)
- Minimum 1GB RAM (Resource constraints are explicitly set in `docker-compose.yml` to prevent the JVM from consuming unbounded host memory)

## Build Process
The build process is defined in the multi-stage `Dockerfile` at the repository root.
1. **Stage 1 (Build)**: Uses a Maven container to resolve dependencies offline, compile the Java code, and package a "fat JAR" with `maven-shade-plugin`. This ensures you do not need Maven installed on your host system.
2. **Stage 2 (Runtime)**: Copies the compiled JAR into a lightweight Alpine Java 21 JRE image. This minimizes the image size and reduces the security surface area.

## Required Environment Variables
*Note: The application currently loads configuration from `src/main/resources/config.yml` built into the JAR. An upcoming refactor is planned to migrate to environment variables.*

For now, you must ensure your `config.yml` is populated with correct values (e.g. `Token`, `AI-Key`) **before** building the Docker image. 

## How to Deploy
1. Ensure `src/main/resources/config.yml` has the correct tokens.
2. Navigate to the `infra/` directory:
   ```bash
   cd infra
   ```
3. Build and start the container in detached mode:
   ```bash
   docker-compose up -d --build
   ```

## Common Maintenance Tasks

### Viewing Logs
The Docker container manages logs using the `json-file` driver. We limit the log size to 10MB per file with a maximum of 3 files to prevent disk exhaustion.
To view logs:
```bash
docker-compose logs -f
```

### Restarting the Bot
If the bot crashes or needs a manual restart (e.g., rate limits):
```bash
docker-compose restart
```

## Update Procedure
When new code is pushed to the repository:
1. Pull the latest code:
   ```bash
   git pull origin main
   ```
2. Rebuild and deploy:
   ```bash
   cd infra
   docker-compose up -d --build
   ```
*Why `--build`?* Docker will see the new source code layers, recompile the JAR, and restart the container seamlessly.

## Rollback Procedure
If a new update breaks the bot, you can rollback to a previous working commit:
1. Identify the last working commit hash:
   ```bash
   git log --oneline
   ```
2. Checkout the specific commit:
   ```bash
   git checkout <COMMIT_HASH>
   ```
3. Rebuild the image for that state:
   ```bash
   cd infra
   docker-compose up -d --build
   ```
4. Once the issue is resolved on `main`, you can `git checkout main` and pull the fixes.
