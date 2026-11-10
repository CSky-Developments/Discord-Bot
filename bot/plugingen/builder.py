import re
import time
from typing import List, Dict, Callable, Optional, Set
from bot.plugingen.models import Project
from bot.plugingen.services.gemini_service import GeminiService
from bot.plugingen.services.generator_service import GeneratorService
from bot.plugingen.services.file_service import FileService
from bot.plugingen.services.build_service import BuildService, BuildResult
from bot.logger import BotLogger

MAX_FIX_ATTEMPTS = 5

class Builder:
    def __init__(self, ai: GeminiService):
        self.ai = ai
        self.generator = GeneratorService()
        self.files = FileService()
        self.compiler = BuildService()

    def build(self, project: Project, logger: Optional[Callable[[str], None]] = None):
        log = logger or (lambda s: BotLogger.info(s, False))

        log(f"[I] Initializing synthesis for system: {project.get_name()}")
        log(f"[I] Target Environment: Spigot {project.get_version()}")

        log("[I] [PHASE 1] Synchronizing project architecture...")
        plan_prompt = self.generator.build_plan_prompt(project)
        plan = self.ai.generate(plan_prompt) or ""

        batches = self.parse_batches(plan, log)
        total_files = sum(len(b) for b in batches)

        log(f"[I] Orchestrating {total_files} modules across {len(batches)} synchronized batches.")

        log("[I] [PHASE 2] Synthesizing source modules...")
        archive: Dict[str, str] = {}

        for batch_num, batch in enumerate(batches):
            log(f"[I] Processing Batch {batch_num + 1}/{len(batches)} ({len(batch)} targets)")

            start = time.time()
            code_prompt = self.generator.build_batch_code_prompt(project, batch, plan, archive)
            raw_response = self.ai.generate(code_prompt)
            duration_ms = int((time.time() - start) * 1000)

            if raw_response:
                log(f"[I]   AI Response: {duration_ms}ms ({len(raw_response)} chars)")
                count = self.parse_and_save_files(project, raw_response, archive, log)
                log(f"[I]   Extracted: {count}/{len(batch)} files")

                if count < len(batch):
                    log("[W]  MISSING FILES!")
                    for requested in batch:
                        if requested not in archive:
                            log(f"[E]    Missing: {requested}")
            else:
                log("[E]  BATCH FAILED (Empty Response)")

            time.sleep(2)

        log(f"[I] Artifact synthesis complete. Total modules: {len(archive)}")

        log("[I] [PHASE 3] Generating documentation...")
        readme_prompt = self.generator.build_readme_prompt(project, archive)
        readme = self.ai.generate(readme_prompt)
        if readme:
            self.files.save_markdown(project, "README.md", readme)
            log(f"[I] Documentation: {len(readme)} chars")

        log("[I] [PHASE 4] Compiling artifact...")

        result: Optional[BuildResult] = None
        for attempt in range(MAX_FIX_ATTEMPTS + 1):
            log(f"[I] Compilation attempt {attempt}/{MAX_FIX_ATTEMPTS}")
            result = self.compiler.build(project)

            if result.success():
                log("[I] Build lifecycle completed successfully.")
                log(f"[I] Artifact Location: {result.path.resolve()}")
                return

            log(f"[W] Compilation failed: {len(result.errors)} errors")

            if attempt < MAX_FIX_ATTEMPTS:
                log(f"[I] AI-assisted fix attempt {attempt + 1}...")

                for error in result.errors:
                    log(f"[B]  ! {error}")

                fix_prompt = self.generator.build_fix_prompt(project, archive, result.errors, plan)
                fix_response = self.ai.generate(fix_prompt)

                if fix_response:
                    fixed = self.parse_and_save_files(project, fix_response, archive, log)
                    log(f"[I]   AI fixed {fixed} files")
                else:
                    log("[W]  AI provided no fixes")

                time.sleep(3)

        log(f"[E] Build lifecycle failed after {MAX_FIX_ATTEMPTS} cycles.")
        if result and result.errors:
            for err in result.errors:
                log(f"[E]  -> {err}")

    def parse_batches(self, plan: str, log: Callable[[str], None]) -> List[List[str]]:
        batches: List[List[str]] = []
        current_batch: Optional[List[str]] = None
        seen_files: Set[str] = set()

        for line in plan.splitlines():
            line = line.strip()

            if line.upper().startswith("BATCH") and ":" in line:
                if current_batch:
                    batches.append(current_batch)
                current_batch = []
                continue

            if line.startswith("-"):
                path = line[1:].strip().split()[0].strip()
                if path and (path.endswith(".java") or path.endswith(".yml")):
                    if current_batch is None:
                        current_batch = []
                    if path not in seen_files:
                        current_batch.append(path)
                        seen_files.add(path)

        if current_batch:
            batches.append(current_batch)

        if not batches:
            log("[W] No batches found in plan, using single batch fallback")
            all_files = self.parse_manifest_flat(plan)
            if all_files:
                batches.append(all_files)

        return batches

    def parse_manifest_flat(self, plan: str) -> List[str]:
        paths: List[str] = []
        for line in plan.splitlines():
            line = line.strip()
            if line.startswith("-"):
                line = line[1:].strip()
            if (".java" in line or ".yml" in line) and "/" in line:
                path = line.split()[0].strip()
                if path:
                    paths.append(path)
        return paths

    def parse_and_save_files(self, project: Project, response: str, archive: Dict[str, str], log: Callable[[str], None]) -> int:
        pattern = re.compile(r"===FILE:(.*?)===\s*([\s\S]*?)===END_FILE===")
        count = 0
        for match in pattern.finditer(response):
            path = match.group(1).strip()
            code = match.group(2).strip()
            self.files.save(project, path, code)
            archive[path] = code
            log(f"[B] + {path} ({len(code)} bytes)")
            count += 1
        return count
