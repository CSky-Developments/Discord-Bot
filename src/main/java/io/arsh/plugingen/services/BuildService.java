package io.arsh.plugingen.services;

import io.arsh.plugingen.models.Project;
import io.arsh.plugingen.utils.Logger;
import javax.tools.*;
import java.io.*;
import java.net.URI;
import java.nio.file.*;
import java.util.*;
import java.util.jar.*;
import java.util.regex.*;

public class BuildService {

    private final Path libDir = Path.of("libs");

    public BuildService() {
        try {
            Files.createDirectories(libDir);
        } catch (IOException ignored) {
        }
    }

    public BuildResult build(Project project) {
        try {
            String version = project.getVersion();
            Path spigotJar = ensureDependency("org.spigotmc", "spigot-api", version);
            Path bungeeChatJar = ensureDependency("net.md-5", "bungeecord-chat", version);

            if (spigotJar == null)
                return new BuildResult(null, List.of("Failed to acquire Spigot API"));

            if (bungeeChatJar == null && version.chars().filter(ch -> ch == '.').count() > 1) {
                String majorMinor = version.substring(0, version.lastIndexOf('.'));
                bungeeChatJar = ensureDependency("net.md-5", "bungeecord-chat", majorMinor);
            }
            if (bungeeChatJar == null) {
                bungeeChatJar = ensureDependency("net.md-5", "bungeecord-chat", "1.21");
            }
            if (bungeeChatJar == null) {
                bungeeChatJar = ensureDependency("net.md-5", "bungeecord-chat", "1.20");
            }

            Logger.debug("Dependencies resolved:");
            Logger.debug(" - Spigot: " + spigotJar.getFileName());
            if (bungeeChatJar != null)
                Logger.debug(" - BungeeChat: " + bungeeChatJar.getFileName());

            Path root = project.getPath();
            Path base = root.resolve("sourcecode").resolve(project.getName());
            Path src = base.resolve("src/main/java");
            Path res = base.resolve("src/main/resources");
            Path bin = base.resolve("target/classes");

            Logger.debug("Compiling source from: " + src);
            Files.createDirectories(bin);

            List<File> javaFiles = Files.walk(src)
                    .filter(p -> p.toString().endsWith(".java"))
                    .map(Path::toFile).toList();

            Logger.info("Compiling " + javaFiles.size() + " source files...");

            if (javaFiles.isEmpty())
                return new BuildResult(null, List.of("No java files"));

            JavaCompiler compiler = ToolProvider.getSystemJavaCompiler();
            List<String> args = new ArrayList<>(List.of("-d", bin.toString(), "--release", "21"));
            args.add("-classpath");

            String cp = spigotJar.toString();
            if (bungeeChatJar != null) {
                cp += File.pathSeparator + bungeeChatJar.toString();
            }
            cp += File.pathSeparator + System.getProperty("java.class.path");
            args.add(cp);

            DiagnosticCollector<JavaFileObject> collector = new DiagnosticCollector<>();
            try (StandardJavaFileManager fm = compiler.getStandardFileManager(collector, null, null)) {
                compiler.getTask(null, fm, collector, args, null, fm.getJavaFileObjectsFromFiles(javaFiles)).call();
            }

            if (collector.getDiagnostics().stream().anyMatch(d -> d.getKind() == Diagnostic.Kind.ERROR)) {
                List<String> errors = collector.getDiagnostics().stream()
                        .filter(d -> d.getKind() == Diagnostic.Kind.ERROR)
                        .map(d -> {
                            String source = "Unknown Source";
                            if (d.getSource() instanceof JavaFileObject jfo) {
                                source = Paths.get(jfo.toUri()).getFileName().toString();
                            }
                            return String.format("[%s:%d:%d] %s",
                                    source,
                                    d.getLineNumber(),
                                    d.getColumnNumber(),
                                    d.getMessage(Locale.ENGLISH));
                        }).toList();

                Logger.error("Build orchestration failed with " + errors.size() + " diagnostics.");
                return new BuildResult(null, errors);
            }
            Logger.info("Class generation complete.");

            if (Files.exists(res)) {
                Files.walk(res).forEach(p -> {
                    try {
                        Path dest = bin.resolve(res.relativize(p));
                        if (Files.isDirectory(p))
                            Files.createDirectories(dest);
                        else
                            Files.copy(p, dest, StandardCopyOption.REPLACE_EXISTING);
                    } catch (IOException ignored) {
                    }
                });
            }

            Path releases = root.resolve("releases");
            Files.createDirectories(releases);
            Path jar = releases.resolve(project.getName() + "-" + project.getVersion() + ".jar");
            Manifest mf = new Manifest();
            mf.getMainAttributes().put(Attributes.Name.MANIFEST_VERSION, "1.0");

            Logger.info("Packaging artifact: " + jar.getFileName());
            try (JarOutputStream jos = new JarOutputStream(Files.newOutputStream(jar), mf)) {
                Files.walk(bin).filter(p -> !Files.isDirectory(p)).forEach(p -> {
                    try {
                        jos.putNextEntry(new JarEntry(bin.relativize(p).toString().replace('\\', '/')));
                        Files.copy(p, jos);
                        jos.closeEntry();
                    } catch (IOException ignored) {
                    }
                });
            }

            return new BuildResult(jar, List.of());
        } catch (Exception ex) {
            ex.printStackTrace();
            return new BuildResult(null, List.of("System Error: " + ex.getMessage()));
        }
    }

    private Path ensureDependency(String groupId, String artifactId, String version) {
        Path jar = libDir.resolve(artifactId + "-" + version + ".jar");
        if (Files.exists(jar))
            return jar;

        String[] repos = {
                "https://hub.spigotmc.org/nexus/content/groups/public/",
                "https://hub.spigotmc.org/nexus/content/repositories/snapshots/"
        };
        String groupPath = groupId.replace('.', '/') + "/" + artifactId + "/";

        Logger.info("Acquiring dependency: " + artifactId + " " + version);

        for (String repo : repos) {
            try {
                Logger.debug("  Checking repo: " + repo);
                String rootMeta = downloadString(repo + groupPath + "maven-metadata.xml");
                String resolvedVersion = null;

                Matcher vMatcher = Pattern.compile("<version>(" + Pattern.quote(version) + ".*?)</version>")
                        .matcher(rootMeta);
                while (vMatcher.find())
                    resolvedVersion = vMatcher.group(1);

                if (resolvedVersion == null) {
                    resolvedVersion = version + "-R0.1-SNAPSHOT";
                    Logger.warn("  Version not found in root metadata, using fallback: " + resolvedVersion);
                }

                String baseFolderUrl = repo + groupPath + resolvedVersion + "/";
                String versionMeta = downloadString(baseFolderUrl + "maven-metadata.xml");

                String ts = extract(versionMeta, "<timestamp>(.*?)</timestamp>");
                String bn = extract(versionMeta, "<buildNumber>(.*?)</buildNumber>");

                String fileName = (ts != null && bn != null)
                        ? artifactId + "-" + resolvedVersion.replace("-SNAPSHOT", "") + "-" + ts + "-" + bn + ".jar"
                        : artifactId + "-" + resolvedVersion + ".jar";

                if (downloadFile(baseFolderUrl + fileName, jar)) {
                    Logger.info("  Downloaded " + artifactId + " " + resolvedVersion);
                    return jar;
                }
            } catch (Exception ignored) {
            }
        }
        return null;
    }

    private String downloadString(String url) throws IOException {
        java.net.HttpURLConnection conn = (java.net.HttpURLConnection) URI.create(url).toURL().openConnection();
        conn.setRequestProperty("User-Agent",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36");
        conn.setRequestProperty("Accept",
                "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8");
        conn.setRequestProperty("Accept-Language", "en-US,en;q=0.9");

        if (conn.getResponseCode() >= 400) {
            throw new IOException("HTTP " + conn.getResponseCode() + " for " + url);
        }

        try (Scanner s = new Scanner(conn.getInputStream()).useDelimiter("\\A")) {
            return s.hasNext() ? s.next() : "";
        }
    }

    private boolean downloadFile(String url, Path target) {
        try {
            java.net.HttpURLConnection conn = (java.net.HttpURLConnection) URI.create(url).toURL().openConnection();
            conn.setRequestProperty("User-Agent",
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36");
            conn.setRequestProperty("Accept", "*/*");

            if (conn.getResponseCode() == 200) {
                try (InputStream in = conn.getInputStream()) {
                    Files.copy(in, target, StandardCopyOption.REPLACE_EXISTING);
                    return true;
                }
            }
        } catch (Exception ignored) {
        }
        return false;
    }

    private String extract(String text, String regex) {
        Matcher m = Pattern.compile(regex).matcher(text);
        return m.find() ? m.group(1) : null;
    }

    public record BuildResult(Path path, List<String> errors) {
        public boolean success() {
            return path != null;
        }
    }
}
