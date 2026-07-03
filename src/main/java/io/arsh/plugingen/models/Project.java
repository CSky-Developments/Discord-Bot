package io.arsh.plugingen.models;

import java.nio.file.Path;
import java.util.UUID;

public class Project {

    private final UUID id;
    private final Path path;

    private final String name;
    private final String version;
    private final String description;

    public Project(String name, String version, String description) {
        this.id = UUID.randomUUID();
        this.path = Path.of("./plugins/" + name + "-" + id.toString());
        this.name = name;
        this.version = version;
        this.description = description;
    }

    public UUID getId() {
        return id;
    }

    public Path getPath() {
        return path;
    }

    public String getName() {
        return name;
    }

    public String getVersion() {
        return version;
    }

    public String getDescription() {
        return description;
    }

}
