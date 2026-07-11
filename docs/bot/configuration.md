# Configuration

The bot relies heavily on runtime configurations to function securely without hardcoding variables.

## Migration to Environment Variables

Historically, sensitive tokens and keys were stored in `config.yml`. This practice has been **deprecated** to prevent credential leaks.
Currently, `io.arsh.utils.Config` manages static configuration loading. We are in the process of transitioning all secret retrieval to use `System.getenv()` directly.

### Required Environment Variables

When running via Docker, ensure these are supplied in your `.env` file (which maps to `docker-compose.yml`):
- `DISCORD_TOKEN`: The API token for the Discord bot.
- `GEMINI_API_KEY`: Google GenAI API key for plugin generation.
- `PUID` & `PGID`: Dynamically assigned host user and group IDs to ensure proper file permissions on mounted volumes.

### `config.yml` (Legacy)
Non-sensitive configuration (like default embed colors, command prefixes, or static channel IDs) should be the only information kept in `src/main/resources/config.yml`.
