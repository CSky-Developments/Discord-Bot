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
The application strictly relies on standard environment variables for configuration. `config.yml` is no longer required in production.

An `.env` file must be created on the VPS at `/srv/services/discord-bot/infra/.env` containing the following:
```env
# Populate PUID and PGID using: id -u csky and id -g csky
PUID=
PGID=
DISCORD_TOKEN=your_token
GUILD_ID=your_guild_id
LOG_CHANNEL_ID=your_log_channel
MEMBER_COUNT_CHANNEL_ID=your_member_channel
COUNTING_CHANNEL_ID=your_counting_channel
STAFF_ROLE_ID=your_staff_role
MEMBER_ROLE_ID=your_member_role
AI_KEY=your_gemini_key
SUPPORT_CATEGORY_ID=your_support_category
TICKET_CHANNEL_ID=your_ticket_channel
TICKET_NORMAL_CATEGORY=your_ticket_category
TICKET_ORDER_CATEGORY=your_ticket_category
TICKET_PLUGIN_GEN_CATEGORY=your_ticket_category
TICKET_REWARD_CATEGORY=your_ticket_category
TICKET_STAFF_APP_CATEGORY=your_ticket_category
PLUGIN_GEN_ACCESS_ROLE_ID=your_role_id
LICENSE_GEN_ACCESS_IDS=id1,id2,id3
```

## How to Deploy (CI/CD)
Deployments are fully automated via GitHub Actions.

1. Create a Pull Request or push code directly to the `main` branch.
2. The `Deploy Bot to VPS` GitHub Action will automatically trigger.
3. It will:
   - Build the Docker image.
   - Push the image to GitHub Container Registry (`ghcr.io`).
   - SSH into the target VPS.
   - Run `docker compose pull` and `docker compose up -d` in the `/srv/services/discord-bot/infra` directory.

No manual intervention is required to deploy new code. The VPS never builds Java code; it simply pulls the latest compiled Docker image.

## Persistent Data (Volumes) & Permissions
Stateful bot data (such as counting games, invites, and tickets) are mapped to `../data` (deployed at `/srv/services/discord-bot/data` on the host). The application runs strictly as the host `csky` user, explicitly resolving the permission issues caused by Docker's root behavior. 

By defining `PUID` and `PGID` in the `.env` file, the container inherits the exact permissions needed to read and write to the host's local data directory. Ephemeral data (`plugins/`, `license.key`) are explicitly written to the system's `/tmp` directory instead of the application directory, keeping the runtime container strictly read-only and stateless.

## Common Maintenance Tasks

### Viewing Logs
The Docker container manages logs using the `json-file` driver. We limit the log size to 10MB per file with a maximum of 3 files to prevent disk exhaustion.
To view logs on the VPS:
```bash
cd /srv/services/discord-bot/infra
docker compose logs -f
```

### Restarting the Bot
If the bot crashes or needs a manual restart (e.g., rate limits):
```bash
cd /srv/services/discord-bot/infra
docker compose restart
```

## Rollback Procedure
If a new update breaks the bot, you can rollback to a previous version using the Docker tags stored in GHCR:
1. SSH into the VPS and navigate to `/srv/services/discord-bot/infra`.
2. Edit `docker-compose.yml` and change the image tag from `latest` to a specific short Git SHA (e.g., `image: ghcr.io/csky-developments/discord-bot:a1b2c3d`).
3. Re-deploy the container:
   ```bash
   docker compose pull
   docker compose up -d
   ```
4. Once the issue is resolved on `main`, revert the tag back to `latest` and push code.
