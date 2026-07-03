package io.arsh.plugingen.services;

import io.arsh.plugingen.models.Project;

import java.util.Map;
import java.util.List;

public class GeneratorService {

    public String buildPlanPrompt(Project project) {
        return String.format(
                """
                        You are a Distinguished Minecraft Systems Architect. Your task is to design the file structure for a Spigot plugin.

                        === PROJECT ===
                        Name: %s
                        API Version: %s
                        Description: %s

                        === ARCHITECTURAL STANDARDS ===
                        1. **Modular Design**: Separate concerns into Managers, Listeners, Commands, and Utilities.
                        2. **Dependency Injection**: Design for constructor-based dependency passing.
                        3. **Main Package**: io.arsh.%4$s

                        === OUTPUT FORMAT (STRICT) ===
                        Group files into BATCHES.
                        **STRICT LIMIT**: Max 8 to 10 files per batch. If more are needed, create BATCH 6, 7, etc.
                        Order: Utilities -> Managers -> Main Class -> Commands/Listeners -> Resources.

                        Format:
                        BATCH 1:
                        - src/main/java/io/arsh/%4$s/utils/ExampleUtil.java
                        BATCH 2:
                        - ...

                        === CRITICAL RULES ===
                        - DO NOT generate any source code.
                        - DO NOT write any logic or implementation details.
                        - DO NOT provide descriptions.
                        - ONLY output the BATCH markers and file paths.
                        - FAILURE TO COMPLY WITH "NO CODE" WILL RESULT IN SYSTEM ERROR.
                        """,
                project.getName(),
                project.getVersion(),
                project.getDescription(),
                project.getName().toLowerCase());
    }

    public String buildBatchCodePrompt(Project project, List<String> targetFiles, String plan,
            Map<String, String> archive) {
        StringBuilder sb = new StringBuilder();
        sb.append(
                "You are a Lead Software Engineer. Synthesize the implementation for the following batch of modules.\n\n");

        sb.append("=== PROJECT CONTEXT ===\n");
        sb.append("Project: ").append(project.getName()).append(" (Spigot ").append(project.getVersion()).append(")\n");
        sb.append("Global Architecture Plan:\n").append(plan).append("\n\n");

        sb.append("=== BATCH TARGETS ===\n");
        sb.append("You must implement ALL of the following files in this single response:\n");
        for (String f : targetFiles) {
            sb.append("- ").append(f).append("\n");
        }
        sb.append("\n");

        if (!archive.isEmpty()) {
            sb.append("=== CODEBASE CONTEXT (Previously Generated) ===\n");
            sb.append("Use these existing classes to ensure correct import paths and method calls:\n\n");
            archive.forEach((path, code) -> {
                sb.append("File: ").append(path).append("\n```java\n").append(code).append("\n```\n\n");
            });
        }

        sb.append("=== IMPLEMENTATION RULES ===\n");
        sb.append("1. **Strict Spigot API**: Use ONLY the declared API version. No internal NMS calls.\n");
        sb.append(
                "2. **No Placeholders**: Write fully functional, logic-dense code. No 'TODO' or 'Implement logic here'.\n");
        sb.append("3. **No External Libs**: No Lombok, Guava, or JetBrains annotations.\n");
        sb.append("4. **Java 21 Syntax**: Use modern Java features (switch expressions, var, etc.) if applicable.\n");
        sb.append("5. **Branding**: In the Main class `onEnable`, log 'Synthesized by CSky Developments'.\n");
        sb.append(
                "6. **Colors**: For hex colors use net.md_5.bungee.api.ChatColor.of(\"#RRGGBB\"). For simple colors, use org.bukkit.ChatColor.\n");
        sb.append("7. **Complete Code**: Every file must be complete and compilable. All imports must be present.\n");

        sb.append("\n=== OUTPUT FORMAT (CRITICAL - READ CAREFULLY) ===\n");
        sb.append("For EACH file, output exactly in this format:\n\n");
        sb.append("===FILE:src/main/java/io/arsh/example/Main.java===\n");
        sb.append("package io.arsh.example;\n");
        sb.append("// ... full source code ...\n");
        sb.append("===END_FILE===\n\n");
        sb.append("===FILE:src/main/resources/plugin.yml===\n");
        sb.append("name: Example\n");
        sb.append("// ... full yaml content ...\n");
        sb.append("===END_FILE===\n\n");
        sb.append("RULES:\n");
        sb.append("1. Each file MUST start with ===FILE:path=== and end with ===END_FILE===\n");
        sb.append("2. Do NOT use markdown code blocks (no triple backticks)\n");
        sb.append("3. Output ONLY the file markers and raw code\n");
        sb.append("4. No explanations before or after the files\n");

        return sb.toString();
    }

    public String buildReadmePrompt(Project project, Map<String, String> archive) {
        StringBuilder sb = new StringBuilder();
        sb.append(
                "You are a Technical Documentation Specialist. Write a professional README.md for this Spigot plugin.\n\n");

        sb.append("=== PROJECT SPECS ===\n");
        sb.append("Name: ").append(project.getName()).append("\n");
        sb.append("API Version: ").append(project.getVersion()).append("\n");
        sb.append("Description: ").append(project.getDescription()).append("\n\n");

        sb.append("=== GENERATED SOURCE CODE ===\n");
        sb.append("The following code has been synthesized. Use this to write accurate documentation.\n\n");

        if (!archive.isEmpty()) {
            archive.forEach((path, code) -> {
                if (code.length() < 3000) {
                    sb.append("File: ").append(path).append("\n```java\n").append(code).append("\n```\n\n");
                }
            });
        }

        sb.append("=== REQUIREMENTS ===\n");
        sb.append("1. Sections: Overview, Features, Installation, Usage/Commands.\n");
        sb.append("2. Content must be USER-FOCUSED (for the person using the plugin, not the developer).\n");
        sb.append("3. STRICT LIMIT: Under 1500 characters total.\n");
        sb.append("4. Format: Standard Markdown.\n");
        sb.append("5. DO NOT include any Java source code or implementation details in the output.\n");
        sb.append("6. Use the provided code ONLY to infer the features and commands.\n");

        sb.append("\nOUTPUT:\n");
        sb.append("Return ONLY the markdown content.\n");

        return sb.toString();
    }

    public String buildFixPrompt(Project project, Map<String, String> failedFiles, List<String> errors, String plan) {
        StringBuilder sb = new StringBuilder();
        sb.append("You are a Senior Systems Debugger. Your task is to analyze and resolve compilation failures.\n\n");

        sb.append("=== SYSTEM CONTEXT ===\n");
        sb.append("Project: ").append(project.getName()).append(" (Spigot ").append(project.getVersion())
                .append(")\n\n");

        sb.append("=== CRITICAL DIAGNOSTICS ===\n");
        for (String error : errors) {
            sb.append("| ERROR | ").append(error).append("\n");
        }
        sb.append("\n");

        sb.append("=== SOURCE MODULES ===\n");
        failedFiles.forEach((path, code) -> {
            sb.append("===FILE:").append(path).append("===\n");
            sb.append(code).append("\n");
            sb.append("===END_FILE===\n\n");
        });

        sb.append("=== FIX PROTOCOL ===\n");
        sb.append("1. **Analysis Phase**: First, provide a technical breakdown of why the errors occurred.\n");
        sb.append(
                "2. **Strategy Phase**: Explain your plan to resolve these specific issues without breaking other modules.\n");
        sb.append("3. **Implementation Phase**: Provide the COMPLETE fixed files. No partial snippets.\n");
        sb.append("4. **Standards**: Maintain Java 21 features and strict Spigot API compliance.\n\n");

        sb.append("=== RESPONSE FORMAT ===\n");
        sb.append("## FIX ANALYSIS & STRATEGY\n");
        sb.append("[Your tactical breakdown here]\n\n");
        sb.append("===FILE:path===\n");
        sb.append("[COMPLETE FIXED CODE]\n");
        sb.append("===END_FILE===\n");

        return sb.toString();
    }
}
