package io.arsh.plugingen.services;

import com.google.genai.Client;
import io.arsh.plugingen.utils.Logger;

public class GeminiService {

    private final Client client;
    private Model model;
    private int modelIndex = 0;

    public GeminiService(String API_KEY) {
        this.client = Client.builder().apiKey(API_KEY).build();
        model = Model.GEMINI_3_FLASH_PREVIEW;
    }

    public boolean isAvailable() {
        return client != null;
    }

    public String generate(String prompt) {
        int retries = 5;
        long cooldown = 10_000;

        Model[] models = Model.values();

        for (int attempt = 1; attempt <= retries; attempt++) {
            try {
                return client.models.generateContent(model.name, prompt, null).text();

            } catch (Exception ex) {
                String msg = ex.getMessage() != null ? ex.getMessage() : "Unknown error";

                if (msg.contains("429") || msg.contains("Quota") || msg.contains("Too Many")) {
                    modelIndex++;
                    Logger.warn("Quota limit reached for " + model.name + ". Switching model...");
                    if (modelIndex < models.length) {
                        model = models[modelIndex];
                        Logger.warn("Switched to model: " + model.name);
                        continue;
                    }
                    Logger.warn("No model left to switch!");
                    break;
                }

                if (msg.contains("503") || msg.contains("overloaded")) {
                    if (attempt < retries) {
                        Logger.warn(String.format(
                                "Service overloaded. Retrying in %d seconds... (%d/%d)",
                                cooldown / 1000, attempt, retries
                        ));
                        sleep(cooldown);
                        cooldown *= 2;
                        continue;
                    }
                }

                Logger.error("Request failed: " + msg);
                Logger.warn(String.format("Waiting for %s seconds before retrying... [%s/%s]", cooldown / 1000, attempt, retries));
                sleep(cooldown);
                cooldown *= 2;
            }
        }

        Logger.error("FAILED TO GENERATE");
        System.exit(0);
        return null;
    }

    private void sleep(long ms) {
        try {
            Thread.sleep(ms);
        } catch (InterruptedException ignored) {
            Thread.currentThread().interrupt();
        }
    }

    private enum Model {
        GEMINI_3_FLASH_PREVIEW("gemini-3-flash-preview"),
        GEMINI_2_5_FLASH("gemini-2.5-flash"),
        GEMINI_2_5_FLASH_LITE("gemini-2.5-flash-lite");

        public final String name;

        Model(String name) {
            this.name = name;
        }
    }

}
