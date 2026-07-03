# CSky Developments Discord Bot

A custom Discord bot tailored for CSky Developments. This monolithic Java application handles community features, administrative tasks, and AI integrations.

## Features
- **Tickets**: Comprehensive support ticketing system.
- **Invites**: Tracks user invites and persistence.
- **Counting Game**: Manages channel-based counting minigames.
- **License Generation**: AES-encrypted license key generation for products.
- **Plugin Generator**: AI-powered Minecraft plugin generator using Google Gemini.

## Tech Stack
- Java 21
- Maven
- JDA (Java Discord API) 5.6.1
- Google GenAI API

## Local Development
To run this project locally for development:
1. Ensure Java 21 and Maven are installed.
2. Create or modify `src/main/resources/config.yml` with your Discord Token and AI Keys.
3. Build the project using Maven:
   ```bash
   mvn clean package
   ```
4. Run the generated fat JAR:
   ```bash
   java -jar target/arsh-1.0-SNAPSHOT.jar
   ```

## Production Deployment
This repository is configured for automated CI/CD deployments using Docker and GitHub Actions.

For detailed instructions on how the deployment pipeline works, the required VPS infrastructure, and rollback procedures, please see our [Deployment Guide](infra/DEPLOYMENT.md).

## AI Maintainers
This project utilizes AI agents for long-term maintenance. If you are an AI agent joining this repository, you **must** read [AGENTS.md](AGENTS.md) before making any architectural or workflow decisions.
