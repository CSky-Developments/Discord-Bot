package io.arsh.plugingen;

import io.arsh.plugingen.models.Project;
import io.arsh.plugingen.services.BuildService;
import io.arsh.plugingen.services.FileService;
import io.arsh.plugingen.services.GeminiService;
import io.arsh.plugingen.services.GeneratorService;
import io.arsh.utils.Logger;

import java.util.*;
import java.util.function.Consumer;
import java.util.regex.*;

public class Builder {

    private final GeminiService ai;
    private final GeneratorService generator;
    private final FileService files;
    private final BuildService compiler;

    private static final int MAX_FIX_ATTEMPTS = 5;

    public Builder(GeminiService ai) {
        this.ai = ai;
        this.generator = new GeneratorService();
        this.files = new FileService();
        this.compiler = new BuildService();
    }

    public void build(Project project) {
        build(project,  (s) -> Logger.info(s, false));
    }

    public void build(Project project, Consumer<String> logger) {
        logger.accept("[I] Initializing synthesis for system: " + project.getName());
        logger.accept("[I] Target Environment: Spigot " + project.getVersion());

        logger.accept("[I] [PHASE 1] Synchronizing project architecture...");
        String planPrompt = generator.buildPlanPrompt(project);
        String plan = ai.generate(planPrompt);

        List<List<String>> batches = parseBatches(plan, logger);
        int totalFiles = batches.stream().mapToInt(List::size).sum();

        logger.accept("[I] " +
                String.format("Orchestrating %d modules across %d synchronized batches.", totalFiles, batches.size()));

        logger.accept("[I] [PHASE 2] Synthesizing source modules...");
        Map<String, String> archive = new HashMap<>();

        for (int batchNum = 0; batchNum < batches.size(); batchNum++) {
            List<String> batch = batches.get(batchNum);
            logger.accept("[I] " +
                    String.format("Processing Batch %d/%d (%d targets)", batchNum + 1, batches.size(), batch.size()));

            long start = System.currentTimeMillis();
            String codePrompt = generator.buildBatchCodePrompt(project, batch, plan, archive);
            String rawResponse = ai.generate(codePrompt);
            long duration = System.currentTimeMillis() - start;

            if (rawResponse != null && !rawResponse.isEmpty()) {
                logger.accept("[I] " +String.format("  AI Response: %dms (%d chars)", duration, rawResponse.length()));
                int count = parseAndSaveFiles(project, rawResponse, archive, logger);
                logger.accept("[I] " +String.format("  Extracted: %d/%d files", count, batch.size()));

                if (count < batch.size()) {
                    logger.accept("[W]  MISSING FILES!");
                    for (String requested : batch) {
                        if (!archive.containsKey(requested)) {
                            logger.accept("[E]    Missing: " + requested);
                        }
                    }
                }
            } else {
                logger.accept("[E]  BATCH FAILED (Empty Response)");
            }

            sleep(2000);
        }

        logger.accept("[I] Artifact synthesis complete. Total modules: " + archive.size());

        logger.accept("[I] [PHASE 3] Generating documentation...");
        String readmePrompt = generator.buildReadmePrompt(project, archive);
        String readme = ai.generate(readmePrompt);
        if (readme != null) {
            files.saveMarkdown(project, "README.md", readme);
            logger.accept("[I] Documentation: " + readme.length() + " chars");
        }

        logger.accept("[I] [PHASE 4] Compiling artifact...");

        BuildService.BuildResult result = null;
        for (int attempt = 0; attempt <= MAX_FIX_ATTEMPTS; attempt++) {
            logger.accept("[I] Compilation attempt " + attempt + "/" + MAX_FIX_ATTEMPTS);
            result = compiler.build(project);

            if (result.success()) {
                logger.accept("[I] Build lifecycle completed successfully.");
                logger.accept("[I] Artifact Location: " + result.path().toAbsolutePath());
                return;
            }

            logger.accept("[W]Compilation failed: " + result.errors().size() + " errors");

            if (attempt < MAX_FIX_ATTEMPTS) {
                logger.accept("[I] AI-assisted fix attempt " + (attempt + 1) + "...");

                for (String error : result.errors()) {
                    logger.accept("[B]  ! " + error);
                }

                String fixPrompt = generator.buildFixPrompt(project, archive, result.errors(), plan);
                String fixResponse = ai.generate(fixPrompt);

                if (fixResponse != null && !fixResponse.isEmpty()) {
                    int fixed = parseAndSaveFiles(project, fixResponse, archive, logger);
                    logger.accept("[I]   AI fixed " + fixed + " files");
                } else {
                    logger.accept("[W]  AI provided no fixes");
                }

                sleep(3000);
            }
        }

        logger.accept("[E]Build lifecycle failed after " + MAX_FIX_ATTEMPTS + " cycles.");
        result.errors().forEach(err -> logger.accept("[E]  -> " + err));
    }

    private List<List<String>> parseBatches(String plan, Consumer<String> logger) {
        List<List<String>> batches = new ArrayList<>();
        List<String> currentBatch = null;
        Set<String> seenFiles = new HashSet<>();

        for (String line : plan.split("\n")) {
            line = line.trim();

            if (line.toUpperCase().startsWith("BATCH") && line.contains(":")) {
                if (currentBatch != null && !currentBatch.isEmpty()) {
                    batches.add(currentBatch);
                }
                currentBatch = new ArrayList<>();
                continue;
            }

            if (line.startsWith("-")) {
                String path = line.substring(1).trim();
                path = path.split("\\s+")[0].trim();

                if (!path.isEmpty() && (path.endsWith(".java") || path.endsWith(".yml"))) {
                    if (currentBatch == null)
                        currentBatch = new ArrayList<>();

                    if (!seenFiles.contains(path)) {
                        currentBatch.add(path);
                        seenFiles.add(path);
                    }
                }
            }
        }

        if (currentBatch != null && !currentBatch.isEmpty()) {
            batches.add(currentBatch);
        }

        if (batches.isEmpty()) {
            logger.accept("[W] No batches found in plan, using single batch fallback");
            List<String> allFiles = parseManifestFlat(plan);
            if (!allFiles.isEmpty()) {
                batches.add(allFiles);
            }
        }

        return batches;
    }

    private List<String> parseManifestFlat(String plan) {
        List<String> paths = new ArrayList<>();
        for (String line : plan.split("\n")) {
            line = line.trim();
            if (line.startsWith("-")) {
                line = line.substring(1).trim();
            }
            if ((line.contains(".java") || line.contains(".yml")) && line.contains("/")) {
                String path = line.split("\\s+")[0].trim();
                if (!path.isEmpty()) {
                    paths.add(path);
                }
            }
        }
        return paths;
    }

    private int parseAndSaveFiles(Project project, String response, Map<String, String> archive, Consumer<String> logger) {
        Matcher m = Pattern.compile("===FILE:(.*?)===\\s*([\\s\\S]*?)===END_FILE===").matcher(response);
        int count = 0;
        while (m.find()) {
            String path = m.group(1).trim();
            String code = m.group(2).trim();
            files.save(project, path, code);
            archive.put(path, code);
            logger.accept("[B] + " + path + " (" + code.length() + " bytes)");
            count++;
        }
        return count;
    }

    private void sleep(long ms) {
        try {
            Thread.sleep(ms);
        } catch (InterruptedException ignored) {
        }
    }

}
