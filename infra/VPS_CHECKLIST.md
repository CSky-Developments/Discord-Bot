# VPS Infrastructure Checklist

This repository assumes that the production server (VPS) is managed externally by a dedicated infrastructure repository (handling reverse proxies, firewalls, backups, etc.). 

Before this repository's automated deployment pipeline can succeed, the infrastructure repository must ensure the following requirements are met on the target VPS:

## 1. System Requirements
- [ ] **Docker Engine**: Installed and running (v20+).
- [ ] **Docker Compose**: Installed (v2+ plugin).
- [ ] **Architecture**: x86_64 or ARM64 (matching the Docker image architecture, GitHub Actions builds x86_64 by default).

## 2. Directory Structure
- [ ] Ensure the deployment root directory exists and is writable by the deployment user:
  ```bash
  mkdir -p /opt/csky-discord-bot/infra/data
  ```

## 3. Environment Variables (Secrets)
- [ ] An `.env` file MUST be placed inside `/opt/csky-discord-bot/infra/`.
- [ ] The `.env` file MUST contain all production secrets, strictly formatted:
  ```env
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
- [ ] The mounted volume directory `/opt/csky-discord-bot/infra/data` must be writable by the container. Since the container runs as a non-root user (`botuser`), ensure the permissions are sufficiently open or explicitly owned by the UID used in the container.
