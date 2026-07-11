# Troubleshooting

Common issues and their resolutions for the CSky Discord Bot.

### Bot goes offline immediately upon startup
**Symptom**: Process exits with code `1`.
**Fix**: 
1. Check `/app/logs/service.log` or `docker compose logs bot`. 
2. Verify `DISCORD_TOKEN` in the `.env` file. JDA will immediately terminate if the token is invalid or missing.

### Plugin generation returns an error
**Symptom**: User invokes AI generation but receives a failure embed.
**Fix**:
1. Check if the `GEMINI_API_KEY` is present and not rate-limited.
2. Verify network connectivity to Google's API endpoints.

### Logs or Data files throwing Permission Denied
**Symptom**: Cannot create files inside `/app/logs/` or `/app/data/`.
**Fix**:
1. Ensure the `PUID` and `PGID` injected into `docker-compose.yml` match the host machine directory owner.
2. Use `ls -ln` on the host to verify owner IDs.

### AI features taking too long to respond
**Symptom**: Discord shows "Interaction Failed".
**Fix**: The `google-genai` integration request must be deferred. Ensure `event.deferReply().queue()` is being called *before* the synchronous API call happens in the code.
