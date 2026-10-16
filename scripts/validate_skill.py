"""Validate this repository's skill format and inspect a reproducible ZIP."""

import hashlib
import json
import re
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "outreachgenie-list-audit"
SKILL = ROOT / "skills" / SKILL_NAME
EXPECTED = {
    "LICENSE",
    "SKILL.md",
    "agents/openai.yaml",
    "fixtures/fictional-snapshot.json",
    "references/capture.md",
    "references/checks.md",
    "references/setup.md",
    "scripts/audit.py",
    "scripts/test_audit.py",
}


def require(condition, message):
    if not condition:
        raise SystemExit(message)


def main():
    require(SKILL.is_dir(), "Skill directory is missing.")
    entries = list(SKILL.rglob("*"))
    require(
        not any(path.is_symlink() for path in entries),
        "Symlinks are not allowed in the package.",
    )
    files = {
        path.relative_to(SKILL).as_posix(): path for path in entries if path.is_file()
    }
    require(
        set(files) == EXPECTED,
        "Unexpected or missing package files; review the explicit package manifest.",
    )
    for relative, path in files.items():
        require(
            path.stat().st_size < 1024 * 1024, f"Package file is too large: {relative}"
        )
        text = path.read_text(encoding="utf-8")
        require(
            re.search(r"(?:/home/[^/\s]+/|/Users/[^/\s]+/)", text) is None,
            f"Private checkout reference in {relative}",
        )
        require(
            re.search(r"-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----", text) is None,
            f"Private key material in {relative}",
        )
    source = files["SKILL.md"].read_text(encoding="utf-8")
    require(source.startswith("---\n"), "SKILL.md must start with YAML frontmatter.")
    parts = source.split("---\n", 2)
    require(len(parts) == 3, "SKILL.md frontmatter is not closed.")
    frontmatter = dict(re.findall(r"^([a-z_]+): (.+)$", parts[1], flags=re.MULTILINE))
    require(
        set(frontmatter) == {"name", "description"},
        "Expected name and description frontmatter.",
    )
    require(
        frontmatter["name"] == SKILL_NAME, "Skill name does not match its directory."
    )
    require(
        20 <= len(frontmatter["description"]) <= 1024,
        "Description must describe the actual task.",
    )
    require(
        "TODO" not in source and "[Replace" not in source, "Unfinished skill scaffold."
    )
    for link in re.findall(r"\]\((references/[^)]+)\)", source):
        require(link in files, f"Missing linked reference: {link}")
    ui = files["agents/openai.yaml"].read_text(encoding="utf-8")
    require("$" + SKILL_NAME in ui, "Codex default prompt must name the skill.")
    fixture = json.loads(files["fixtures/fictional-snapshot.json"].read_text())
    require(
        fixture.get("source_kind") == "fictional_fixture",
        "Only the fictional fixture belongs in the package.",
    )
    require(
        fixture.get("schema_version") == 1, "Fixture schema changed; review validation."
    )
    require(
        "MIT License" in files["LICENSE"].read_text(),
        "Expected the repository's MIT license.",
    )
    with tempfile.TemporaryDirectory(prefix="outreachgenie-skill-package-") as temp:
        archive = Path(temp) / (SKILL_NAME + ".zip")
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
            for relative, path in sorted(files.items()):
                info = zipfile.ZipInfo(
                    f"{SKILL_NAME}/{relative}", date_time=(2026, 10, 16, 0, 0, 0)
                )
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                bundle.writestr(info, path.read_bytes())
        with zipfile.ZipFile(archive) as bundle:
            require(bundle.testzip() is None, "ZIP integrity check failed.")
            require(len(bundle.namelist()) == len(EXPECTED), "ZIP manifest mismatch.")
            for item in bundle.infolist():
                path = PurePosixPath(item.filename)
                require(
                    not path.is_absolute()
                    and ".." not in path.parts
                    and path.parts[0] == SKILL_NAME,
                    "Unsafe ZIP path.",
                )
                require(
                    (item.external_attr >> 16) & 0o170000 != 0o120000,
                    "ZIP contains a symlink.",
                )
        print(
            json.dumps(
                {
                    "skill": SKILL_NAME,
                    "files": len(files),
                    "zip_sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
                    "network_required": False,
                }
            )
        )


if __name__ == "__main__":
    main()
