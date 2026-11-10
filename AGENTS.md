# Project Overview

- **Purpose of the project**: A custom Discord bot built for "CSky Developments" that manages tickets, invites, counting minigames, and AI-assisted plugin generation.
- **High-level architecture**: A monolithic Discord application leveraging discord.py. Event listeners are modularized by feature (e.g., TicketManager, InviteTracker, AIListener). Configuration is driven by environment variables and a fallback config.yml.
- **Technology stack**: 
  - Python 3.12+
  - discord.py 2.4+ (Discord API wrapper)
  - Google GenAI SDK (google-genai 1.0+)
  - PyYAML 6.0+
  - OpenJDK 21 headless (for runtime Spigot plugin builds via javac)

# Repository Structure

- `bot/` - Root Python package
  - `main.py` - Application entry point; initializes bot, sets up presence, commands, and event listeners.
  - `config.py` - Configuration parsing with YAML fallback and environment variable overrides.
  - `logger.py` - Bot logging with console output, file rotation, and Discord channel logging.
  - `ai/` - AI integration logic (Google Gemini 2.5 Flash).
  - `commands/` - Slash command registration and handlers.
  - `embeds/` - Discord Embed templates with exact colors, fields, and footers.
  - `game/` - Minigames like Counting with atomic JSON persistence.
  - `invite/` - Tracks user invites and persistence.
  - `message/` - Message caching and audit logging.
  - `plugingen/` - AI-powered plugin generator workflow, invoking Gemini and build services.
  - `ticket/` - Support ticket management.
- `tests/` - Comprehensive unit test suite with pytest.
- `infra/` - Deployment configs (`docker-compose.yml`, `.env.example`).
- `Dockerfile` - Multi-runtime Dockerfile (Python 3.12 + OpenJDK 21 headless).

# Development Conventions

- **Coding style**: Standard Java conventions (PascalCase for classes, camelCase for methods and variables).
- **Naming conventions**: Descriptive class names mapped to features (e.g., `TicketManager`, `InviteTracker`).
- **Error handling conventions**: 
  - During startup (`Main.java`), exceptions are caught, logged, and trigger a `System.exit(1)`.
  - Runtime errors are typically logged using the custom `Logger` utility.
- **Logging conventions**: Handled by `io.arsh.utils.Logger`, which supports both console logging and pushing logs to a specific Discord channel (`Config.LOG_CHANNEL_ID`).
- **Documentation conventions**: The repository currently lacks comprehensive JavaDocs. Code is mostly self-documenting via naming.

# Architecture Decisions

- **Important design decisions**: 
  - Uses JDA's event-driven architecture heavily.
  - Separates concerns into managers that implement `EventListener`.
  - Configurations are loaded statically into `Config` at startup.
- **Trade-offs**: 
  - Using static fields for Configuration and Logging reduces boilerplate but tightly couples the application and makes testing harder.
- **Patterns currently used**: 
  - Singleton-like static managers (Config, Logger).
  - Observer pattern (JDA Event Listeners).
- **Anti-patterns to avoid**: 
  - Avoid adding more static state. Transition towards Dependency Injection if the project scales further.
  - Avoid raw `System.exit(1)` in standard runtime flow (acceptable only in initialization phases).

# Deployment

- **Runtime requirements**: Java 21 JRE/JDK.
- **Environment variables**: Managed strictly via standard environment variables. `config.yml` is deprecated in production.
- **Docker requirements**: A multi-stage `Dockerfile` and `docker-compose.yml` build an Alpine image.
- **CSky Deployment Standard**:
  - **No root containers**: Applications must run as non-root.
  - **Dynamic host user**: The container does not hardcode UIDs/GIDs. `docker-compose.yml` explicitly specifies `user: "${PUID}:${PGID}"`. Ephemeral data is strictly written to the system `/tmp` directory, preventing the need to `chmod 777` the working directory and keeping the container read-only outside of explicitly mapped volumes.
  - **Persistent storage**: All persistent files must be stored in the service-local data directory (e.g., `/srv/services/discord-bot/data`) and are owned by the `csky` user on the host machine.
  - **Every future CSky service must follow this same convention** to avoid debugging Linux file permissions for bind mounts ever again.
- **Deployment workflow**: GitHub Actions automates building the image, publishing to GHCR, and pulling/running via SSH to the VPS.
- **Scope limitation**: Keep deployment infrastructure limited to this project (Dockerfile, docker-compose.yml, env configs, deployment docs). Assume a separate repo manages VPS, reverse proxy, monitoring, backups, etc. Do not duplicate shared infrastructure here.

# Known Technical Debt

- **Existing issues**: Sensitive tokens and keys were historically stored in `config.yml`. They have been removed, but the configuration loading logic (`Config.java`) still expects them to be in the YAML file rather than system environment variables.
- **Areas needing improvement**: 
  - Transition secret loading from `config.yml` to standard Environment Variables (`System.getenv()`).
  - Implement graceful shutdown hooks instead of abrupt exists.
- **Planned refactors**: 
  - Update `Config.java` to fallback to environment variables.
  - Dockerize the application.

# Working Guidelines for Future AI Agents

- **Preserve the existing coding style**: Stick to the current structure, avoid introducing heavy frameworks (like Spring) unless explicitly requested.
- **Avoid unnecessary architectural changes**: Continue using JDA event listeners. Refactor static state only if it blocks a feature requirement.
- **Keep documentation synchronized with implementation**: Ensure `AGENTS.md` and `infra/DEPLOYMENT.md` reflect actual states.
- **Explain trade-offs before making significant changes**: Always clarify why a change is needed (e.g., moving secrets to ENV variables).
- **Prefer incremental improvements over large rewrites**: Introduce changes slowly and testability.
- **Limit infrastructure scope**: Keep deployment infrastructure limited to this project (Dockerfile, docker-compose.yml, env configs, deployment docs). Assume a separate repo manages VPS, reverse proxy, monitoring, backups, etc. Do not duplicate shared infrastructure here.
- **Never assume numeric UIDs/GIDs**: The deployment user is dynamically assigned by the host infrastructure. Containers must consume `PUID` and `PGID` without fallback defaults (e.g., 1000).

# Change Log

- **2026-07-03**: Initialized `AGENTS.md`. Established AI maintenance protocol. Removed leaked Discord tokens from `config.yml`.
- **2026-11-10**: Translated entire core application from Java to Python (`discord.py`) with 100% functional, cryptographic, and data parity. Implemented comprehensive test suite with 23 pytest tests. Updated Dockerfile to Python 3.12 + OpenJDK 21 headless.
- **2026-11-10**: Completely removed legacy license system, AES crypto modules, license slash command, and associated configs across codebase.
