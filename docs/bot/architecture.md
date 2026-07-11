# Architecture

The CSky Discord Bot is a monolithic Java application designed using **JDA (Java Discord API)**. It heavily utilizes an event-driven architecture, observing Discord events and dispatching them to modular feature managers.

## System Overview

At its core, the bot bootstraps through `io.arsh.Main`, initializing JDA and connecting to the Discord gateway. It registers several discrete listeners for features.

## Feature Modules

- **TicketManager** (`io.arsh.ticket`): Manages the creation, interaction, and archival of support tickets.
- **InviteTracker** (`io.arsh.invite`): Listens to guild member joins and resolves which invite link was used, tracking persistence.
- **Counting Game** (`io.arsh.game`): Validates sequential counting in specific channels.
- **License Generator** (`io.arsh.license`): Securely generates AES-encrypted keys for distributed CSky products.
- **Plugin Generator** (`io.arsh.plugingen`): Integrates with Google GenAI to prompt and generate Java source code for Minecraft plugins based on user input.

## Data Flow
Instead of using a dedicated external database, the bot currently relies on flat-file configurations or simple local caching where appropriate. Future scaling may demand external database integrations (e.g., PostgreSQL or MongoDB).

## AI Integrations
The application integrates the `google-genai` SDK for plugin generation. Prompts are constructed in the `ai` module, and requests are fired asynchronously to prevent blocking the JDA event thread.
