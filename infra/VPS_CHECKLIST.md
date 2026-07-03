# VPS Infrastructure Checklist

This repository assumes that the production server (VPS) is managed externally by a dedicated infrastructure repository (handling reverse proxies, firewalls, backups, etc.). 

Before this repository's automated deployment pipeline can succeed, the infrastructure repository must ensure the following requirements are met on the target VPS:

## 1. System Requirements
- [ ] **Docker Engine**: Installed and running (v20+).
- [ ] **Docker Compose**: Installed (v2+ plugin).
- [ ] **Architecture**: x86_64 or ARM64 (matching the Docker image architecture, GitHub Actions builds x86_64 by default).
- [ ] **GHCR Authentication**: The VPS must be logged into the GitHub Container Registry (`ghcr.io`) using a GitHub Classic PAT with `read:packages` permissions.
  ```bash
  echo "YOUR_GITHUB_PAT" | docker login ghcr.io -u YOUR_GITHUB_USERNAME --password-stdin
  ```

## 2. Directory Structure
- [ ] Ensure the deployment root directory exists and is owned by the `csky` user:
  ```bash
  sudo mkdir -p /srv/csky-discord-bot/data
  sudo chown -R csky:csky /srv/csky-discord-bot
  ```

## 3. Environment Variables (Secrets)
- [ ] An `.env` file MUST be placed alongside your docker-compose.yml (e.g. `/opt/csky-discord-bot/infra/.env`).
- [ ] The `.env` file MUST contain all production secrets, as well as the UID/GID for the `csky` user on the host:
  ```env
  PUID=1000  # Replace with the actual UID of the 'csky' user
  PGID=1000  # Replace with the actual GID of the 'csky' user
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

## 4. SSH Access for GitHub Actions
- [ ] A dedicated deployment user exists (e.g., `deployer`).
- [ ] SSH key pair generated. The public key is in `/home/deployer/.ssh/authorized_keys`.
- [ ] The private key, VPS IP, username, and port are added to this repository's **GitHub Secrets** (`VPS_HOST`, `VPS_USERNAME`, `VPS_SSH_KEY`, `VPS_PORT`).
- [ ] The `deployer` user must be part of the `docker` group to execute `docker compose` commands without `sudo`.

## 5. Docker Permissions
- [ ] The mounted volume directory `/srv/csky-discord-bot/data` must be writable by the `csky` user. Because the container is strictly configured in Docker Compose to run using the `PUID` and `PGID`, the container will seamlessly inherit read/write permissions for the `/srv/csky-discord-bot/data` volume without any manual permission fix-up scripts.
