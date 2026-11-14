# CSky Developments Discord Bot

A custom Discord bot tailored for CSky Developments built with Python 3.12+ and discord.py. This application handles community features, administrative tasks, support tickets, and AI integrations.

## Features
- **Tickets**: Support ticketing system with categories (Support, Order, Staff Application).
- **Web & Store Sync**: `/links`, `/status`, `/store`, and automatic `/claim-buyer` role sync with `store.csky.dev`.
- **Invites**: Tracks user invites, member roles, and persists invite counts.
- **Counting Game**: Channel-based counting minigame with milestone tracking and double-count prevention.
- **Message Auditing**: Non-intrusive LRU audit logger for message deletes and edits.

## Tech Stack
- Python 3.12+
- [discord.py](https://github.com/Rapptz/discord.py) 2.4+
- aiohttp 3.9+
- PyYAML 6.0+
- pytest & pytest-asyncio

## Local Development
To run this project locally for development:
1. Ensure Python 3.12+ is installed.
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Or on Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `config.example.yml` to `config.yml` and provide your credentials, or set environment variables:
   ```bash
   cp config.example.yml config.yml
   ```
5. Run the bot:
   ```bash
   python -m bot.main
   ```

## Running Tests
Run the comprehensive test suite with pytest:
```bash
pytest -v tests
```

## Production Deployment
This repository is configured for automated CI/CD deployments using Docker and GitHub Actions.

For detailed instructions on how the deployment pipeline works, the required VPS infrastructure, and standards, please see our [Deployment Guide](docs/bot/deployment.md).

## AI Maintainers
This project utilizes AI agents for long-term maintenance. If you are an AI agent joining this repository, you **must** read [AGENTS.md](AGENTS.md) before making any architectural or workflow decisions.
