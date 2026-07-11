# Deployment

The Discord Bot is deployed via a CI/CD pipeline using GitHub Actions, packaging the Java application into a Docker container.

## CSky Deployment Standards

All CSky infrastructure services adhere strictly to the following deployment rules:
1. **No Root Containers**: Applications run as non-root users.
2. **Dynamic Host User**: We do not hardcode UIDs/GIDs (e.g. 1000). The container consumes `PUID` and `PGID` directly from the host.
3. **Ephemeral Storage**: Transient data is written to `/tmp`.
4. **Persistent Storage**: Mapped via explicitly bound volumes (e.g., `../data:/app/data`) owned by the `csky` user on the VPS.

## Docker Compose Setup

Located in `infra/docker-compose.yml`, our stack defines resource limits (e.g., `1G` memory) and uses the standard `ghcr.io/csky-developments/discord-bot` image.

To spin it up locally for testing the production environment:
```bash
cd infra
cp .env.example .env
# Edit .env to supply your tokens
docker-compose up -d
```
