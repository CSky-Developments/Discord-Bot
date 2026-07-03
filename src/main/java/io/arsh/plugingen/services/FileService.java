package io.arsh.plugingen.services;

import io.arsh.plugingen.models.Project;
import io.arsh.plugingen.utils.Filter;
import io.arsh.plugingen.utils.Logger;

import java.io.IOException;
import java.nio.file.*;

public class FileService {

    public void save(Project project, String path, String content) {
        Path root = project.getPath().resolve("sourcecode").resolve(project.getName());
        Path target = root.resolve(path);

        final boolean[] foundBlock = { false };

        Filter.clean(content, code -> {
            foundBlock[0] = true;
            try {
                if (target.getParent() != null) {
                    Files.createDirectories(target.getParent());
                }

                if (path.equalsIgnoreCase("README.md")) {
                    Files.writeString(target, content);
                    return;
                }

                Files.writeString(target, code);
            } catch (IOException e) {
                Logger.error("Failed to write " + path + ": " + e.getMessage());
            }
        });

        if (!foundBlock[0] && content != null && !content.isBlank()) {
            try {
                if (target.getParent() != null) {
                    Files.createDirectories(target.getParent());
                }
                Files.writeString(target, content.trim());
            } catch (IOException e) {
                Logger.error("Failed to write raw " + path + ": " + e.getMessage());
            }
        }
    }

    public void saveMarkdown(Project project, String path, String content) {
        Path root = project.getPath().resolve("sourcecode").resolve(project.getName());
        Path target = root.resolve(path);
        try {
            if (target.getParent() != null) {
                Files.createDirectories(target.getParent());
            }
            Files.writeString(target, content);
        } catch (IOException e) {
            Logger.error("Failed to write " + path + ": " + e.getMessage());
        }
    }

}
