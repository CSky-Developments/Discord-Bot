# Logging Standard

In compliance with the **CSky Infrastructure Logging Standard**, this bot implements a highly robust, standardized approach to application observability.

## The Standard Rules

1. **Persistent Storage**: All logs write to `/app/logs/service.log` and are bind-mounted to the host machine.
2. **Standard Format**: `[YYYY-MM-DD HH:mm:ss] [LEVEL] [SERVICE] - Message`.
3. **Startup Archival**: When the bot boots, it archives the previous session's log file by appending its last-modified timestamp (e.g., `service-2026-07-11_10-15-30.log`).
4. **Dual Output**: Logs mirror to `stdout` to allow standard Docker `json-file` log capture.
5. **No Spam**: Polling spam and meaningless heartbeats are actively suppressed.

## Implementation Details
The application utilizes **Logback** and **SLF4J**.
- **`logback.xml`**: Configured with `SizeAndTimeBasedRollingPolicy` capping files at 10MB and holding 14 days of history.
- **Startup Renaming**: A programmatic snippet inside `Main.java` ensures the old `service.log` is securely archived *before* the logger context initializes, preventing Logback from inadvertently clearing it or losing timestamp precision.
- **Legacy Support**: The internal `io.arsh.utils.Logger` still functions, but now acts as an SLF4J wrapper to ensure the Discord webhook functionality remains intact without breaking the new format.
