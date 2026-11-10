import os
import re
import shutil
import zipfile
import subprocess
import urllib.request
from pathlib import Path
from typing import List, Optional, Tuple
from dataclasses import dataclass
from bot.plugingen.models import Project
from bot.logger import BotLogger

@dataclass
class BuildResult:
    path: Optional[Path]
    errors: List[str]

    def success(self) -> bool:
        return self.path is not None

class BuildService:
    def __init__(self, lib_dir: str = "libs"):
        self.lib_dir = Path(lib_dir)
        self.lib_dir.mkdir(parents=True, exist_ok=True)

    def build(self, project: Project) -> BuildResult:
        try:
            version = project.get_version()
            spigot_jar = self.ensure_dependency("org.spigotmc", "spigot-api", version)
            bungee_chat_jar = self.ensure_dependency("net.md-5", "bungeecord-chat", version)

            if not spigot_jar:
                return BuildResult(None, ["Failed to acquire Spigot API"])

            if not bungee_chat_jar and version.count(".") > 1:
                major_minor = version[:version.rfind(".")]
                bungee_chat_jar = self.ensure_dependency("net.md-5", "bungeecord-chat", major_minor)
            if not bungee_chat_jar:
                bungee_chat_jar = self.ensure_dependency("net.md-5", "bungeecord-chat", "1.21")
            if not bungee_chat_jar:
                bungee_chat_jar = self.ensure_dependency("net.md-5", "bungeecord-chat", "1.20")

            BotLogger.debug("Dependencies resolved:")
            BotLogger.debug(f" - Spigot: {spigot_jar.name}")
            if bungee_chat_jar:
                BotLogger.debug(f" - BungeeChat: {bungee_chat_jar.name}")

            root = project.get_path()
            base = root / "sourcecode" / project.get_name()
            src = base / "src" / "main" / "java"
            res = base / "src" / "main" / "resources"
            bin_dir = base / "target" / "classes"

            BotLogger.debug(f"Compiling source from: {src}")
            bin_dir.mkdir(parents=True, exist_ok=True)

            java_files = list(src.rglob("*.java"))
            BotLogger.info(f"Compiling {len(java_files)} source files...")

            if not java_files:
                return BuildResult(None, ["No java files found to compile"])

            cp_parts = [str(spigot_jar)]
            if bungee_chat_jar:
                cp_parts.append(str(bungee_chat_jar))
            classpath = os.pathsep.join(cp_parts)

            cmd = ["javac", "-d", str(bin_dir), "-classpath", classpath]
            # Add --release 21 if supported
            cmd.extend([str(f) for f in java_files])

            proc = subprocess.run(cmd, capture_output=True, text=True)
            if proc.returncode != 0:
                errors = [line.strip() for line in proc.stderr.splitlines() if line.strip()]
                BotLogger.error(f"Build orchestration failed with {len(errors)} diagnostics.")
                return BuildResult(None, errors)

            BotLogger.info("Class generation complete.")

            # Copy resources
            if res.exists():
                for res_file in res.rglob("*"):
                    if res_file.is_file():
                        rel = res_file.relative_to(res)
                        dest = bin_dir / rel
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(res_file, dest)

            releases = root / "releases"
            releases.mkdir(parents=True, exist_ok=True)
            jar_path = releases / f"{project.get_name()}-{project.get_version()}.jar"

            BotLogger.info(f"Packaging artifact: {jar_path.name}")
            with zipfile.ZipFile(jar_path, "w", zipfile.ZIP_DEFLATED) as zf:
                # Add MANIFEST.MF
                manifest_content = "Manifest-Version: 1.0\r\nCreated-By: CSky Developments\r\n\r\n"
                zf.writestr("META-INF/MANIFEST.MF", manifest_content)

                for f in bin_dir.rglob("*"):
                    if f.is_file():
                        arcname = f.relative_to(bin_dir).as_posix()
                        zf.write(f, arcname)

            return BuildResult(jar_path, [])
        except Exception as ex:
            BotLogger.error(f"Build packaging exception: {ex}")
            return BuildResult(None, [f"System Error: {ex}"])

    def ensure_dependency(self, group_id: str, artifact_id: str, version: str) -> Optional[Path]:
        jar_path = self.lib_dir / f"{artifact_id}-{version}.jar"
        if jar_path.exists():
            return jar_path

        repos = [
            "https://hub.spigotmc.org/nexus/content/groups/public/",
            "https://hub.spigotmc.org/nexus/content/repositories/snapshots/"
        ]
        group_path = group_id.replace(".", "/") + "/" + artifact_id + "/"

        BotLogger.info(f"Acquiring dependency: {artifact_id} {version}")

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "*/*"
        }

        for repo in repos:
            try:
                root_meta_url = repo + group_path + "maven-metadata.xml"
                req = urllib.request.Request(root_meta_url, headers=headers)
                with urllib.request.urlopen(req, timeout=10) as resp:
                    root_meta = resp.read().decode("utf-8", errors="ignore")

                resolved_version = None
                v_matches = re.findall(rf"<version>({re.escape(version)}.*?)</version>", root_meta)
                if v_matches:
                    resolved_version = v_matches[-1]

                if not resolved_version:
                    resolved_version = f"{version}-R0.1-SNAPSHOT"

                base_folder_url = repo + group_path + resolved_version + "/"
                try:
                    req_meta = urllib.request.Request(base_folder_url + "maven-metadata.xml", headers=headers)
                    with urllib.request.urlopen(req_meta, timeout=10) as resp_meta:
                        version_meta = resp_meta.read().decode("utf-8", errors="ignore")

                    ts_match = re.search(r"<timestamp>(.*?)</timestamp>", version_meta)
                    bn_match = re.search(r"<buildNumber>(.*?)</buildNumber>", version_meta)
                    ts = ts_match.group(1) if ts_match else None
                    bn = bn_match.group(1) if bn_match else None

                    if ts and bn:
                        file_name = f"{artifact_id}-{resolved_version.replace('-SNAPSHOT', '')}-{ts}-{bn}.jar"
                    else:
                        file_name = f"{artifact_id}-{resolved_version}.jar"
                except Exception:
                    file_name = f"{artifact_id}-{resolved_version}.jar"

                jar_url = base_folder_url + file_name
                req_jar = urllib.request.Request(jar_url, headers=headers)
                with urllib.request.urlopen(req_jar, timeout=30) as resp_jar, open(jar_path, "wb") as out_file:
                    shutil.copyfileobj(resp_jar, out_file)

                if jar_path.exists() and jar_path.stat().st_size > 1000:
                    BotLogger.info(f"  Downloaded {artifact_id} {resolved_version}")
                    return jar_path
                else:
                    if jar_path.exists():
                        jar_path.unlink()
            except Exception:
                pass

        return None
