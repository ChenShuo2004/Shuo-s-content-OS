#!/usr/bin/env python3
"""
Small dependency-free CLI for Chuo's Content OS.

The tool manages files and state. It does not make scoring decisions for you.
Use it to preserve the workflow discipline: write predictions before data, then
append retrospectives after actuals arrive.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


VERSION = "0.1.0"
STATE_FILE = ".content-os-state.json"
ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = ROOT / "templates"


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def today() -> str:
    return datetime.now().astimezone().date().isoformat()


def sha12(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def file_hash12(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text[:48] or "piece"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str, force: bool = False) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        return False
    path.write_text(text, encoding="utf-8", newline="\n")
    return True


def render_template(name: str, mapping: dict[str, object]) -> str:
    text = read_text(TEMPLATE_DIR / name)
    for key, value in mapping.items():
        text = text.replace("{{" + key + "}}", str(value))
    return text


def project_path(path: str | Path) -> Path:
    return Path(path).expanduser().resolve()


def inside_project(project: Path, path: str | Path) -> Path:
    raw = Path(path).expanduser()
    if raw.is_absolute():
        return raw.resolve()
    return (project / raw).resolve()


def rel_to_project(project: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(project.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def state_path(project: Path) -> Path:
    return project / STATE_FILE


def load_state(project: Path) -> dict:
    path = state_path(project)
    if not path.exists():
        raise SystemExit(f"error: {project} is not initialized. Run: content_os.py init {project}")
    return json.loads(read_text(path))


def save_state(project: Path, state: dict) -> None:
    path = state_path(project)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    tmp.replace(path)


def first_heading(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip() or fallback
    return fallback


def first_body_summary(text: str, limit: int = 400) -> str:
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("**"):
            continue
        if stripped.startswith("[") and stripped.endswith("]"):
            continue
        lines.append(stripped)
        if sum(len(x) for x in lines) >= limit:
            break
    summary = " ".join(lines).strip()
    return summary[:limit] if summary else "TBD"


def content_id_from_script(script: Path, text: str) -> str:
    match = re.match(r"^\d{4}-\d{2}-\d{2}_([0-9a-f]{12})_", script.name)
    if match:
        return match.group(1)
    return sha12(text)


def confidence_label(samples: int) -> str:
    if samples <= 0:
        return "very-low"
    if samples <= 2:
        return "low"
    if samples <= 5:
        return "medium-low"
    if samples <= 10:
        return "medium"
    if samples <= 20:
        return "high-ish"
    return "high"


def parse_predicted_center(text: str) -> float | None:
    match = re.search(r"\*\*Predicted Center\*\*:\s*`?([0-9]+(?:\.[0-9]+)?)`?", text)
    if not match:
        return None
    return float(match.group(1))


def prediction_has_completed_retro(text: str) -> bool:
    match = re.search(r"## Retro\s*(.*)", text, flags=re.DOTALL)
    if not match:
        return False
    return "Pending." not in match.group(1)


def replace_or_append_publish(text: str, section: str) -> str:
    pending = "## Publish\n\nPending."
    if pending in text:
        return text.replace(pending, section.strip(), 1)
    if "## Publish" in text:
        return text.rstrip() + "\n\n" + section.strip() + "\n"
    return text.rstrip() + "\n\n" + section.strip() + "\n"


def replace_or_append_retro(text: str, section: str, force: bool = False) -> str:
    pending = "## Retro\n\nPending."
    if pending in text:
        return text.replace(pending, section.strip(), 1)
    if "## Retro" in text and not force:
        raise SystemExit("error: retro already exists. Refusing to edit an existing retro without --force.")
    return text.rstrip() + "\n\n" + section.strip() + "\n"


def cmd_init(args: argparse.Namespace) -> int:
    project = project_path(args.project)
    project.mkdir(parents=True, exist_ok=True)

    for folder in ("scripts", "predictions", "retros", "videos", "assets", "exports"):
        (project / folder).mkdir(parents=True, exist_ok=True)

    mapping = {
        "PROJECT_NAME": project.name,
        "DEFAULT_PLATFORM": args.default_platform or os.environ.get("CONTENT_OS_DEFAULT_PLATFORM", "manual"),
        "TIMEZONE": os.environ.get("CONTENT_OS_TIMEZONE", "local"),
        "INITIALIZED_AT": now_iso(),
    }

    created: list[str] = []
    skipped: list[str] = []

    files = {
        ".gitignore": ("project/gitignore.template", {}),
        "WORKFLOW.md": ("project/WORKFLOW.md", {}),
        "STATUS.md": ("project/STATUS.md", {}),
        "rubric.md": ("project/rubric.md", {}),
        "rubric-memo.md": ("project/rubric-memo.md", {}),
        "candidates.md": ("project/candidates.md", {}),
        "audience.md": ("project/audience.md", {}),
        "script_patterns.md": ("project/script_patterns.md", {}),
        STATE_FILE: ("state.json", mapping),
    }

    for dest_name, (template_name, extra) in files.items():
        dest = project / dest_name
        text = render_template(template_name, {**mapping, **extra})
        if write_text(dest, text, force=args.force):
            created.append(dest_name)
        else:
            skipped.append(dest_name)

    print(f"initialized: {project}")
    if created:
        print("created:")
        for item in created:
            print(f"  {item}")
    if skipped:
        print("skipped existing:")
        for item in skipped:
            print(f"  {item}")
    return 0


def cmd_new_script(args: argparse.Namespace) -> int:
    project = project_path(args.project)
    state = load_state(project)
    content_id = sha12(f"{args.title}|{now_iso()}")
    filename = f"{today()}_{content_id}_{slugify(args.title)}.md"
    dest = project / "scripts" / filename

    text = render_template(
        "script.md",
        {
            "TITLE": args.title,
            "CONTENT_ID": content_id,
            "CREATED_AT": now_iso(),
            "CONTENT_FORM": args.form or state.get("content_form", "mixed"),
        },
    )
    if not write_text(dest, text, force=args.force):
        raise SystemExit(f"error: file already exists: {dest}")

    state["last_script_file"] = rel_to_project(project, dest)
    save_state(project, state)
    print(rel_to_project(project, dest))
    return 0


def cmd_predict(args: argparse.Namespace) -> int:
    project = project_path(args.project)
    state = load_state(project)
    script = inside_project(project, args.script)
    if not script.exists():
        raise SystemExit(f"error: script not found: {script}")

    script_text = read_text(script)
    title = first_heading(script_text, script.stem)
    content_id = content_id_from_script(script, script_text)
    dest = project / "predictions" / script.name

    mapping = {
        "TITLE": title,
        "CONTENT_ID": content_id,
        "RUBRIC_VERSION": state.get("rubric_version", "v0"),
        "PREDICTED_AT": now_iso(),
        "SCRIPT_PATH": rel_to_project(project, script),
        "SCRIPT_HASH": file_hash12(script),
        "CALIBRATION_SAMPLES": state.get("calibration_samples", 0),
        "CONFIDENCE": confidence_label(int(state.get("calibration_samples", 0))),
        "SCORES": args.scores or "not scored",
        "DRAFT_SUMMARY": args.summary or first_body_summary(script_text),
        "BUCKET": args.bucket,
        "PREDICTED_CENTER": args.center,
        "REASON": args.reason,
        "P_LOWER": args.p_lower,
        "P_EXPECTED": args.p_expected,
        "P_HIGHER": args.p_higher,
    }
    text = render_template("prediction.md", mapping)
    if not write_text(dest, text, force=args.force):
        raise SystemExit(f"error: prediction already exists: {dest}")

    state["last_prediction_file"] = rel_to_project(project, dest)
    save_state(project, state)
    print(rel_to_project(project, dest))
    return 0


def cmd_publish(args: argparse.Namespace) -> int:
    project = project_path(args.project)
    state = load_state(project)
    prediction = inside_project(project, args.prediction)
    if not prediction.exists():
        raise SystemExit(f"error: prediction not found: {prediction}")

    rel = rel_to_project(project, prediction)
    section = f"""## Publish

**Platform**: `{args.platform}`  
**URL**: {args.url}  
**Published At**: `{now_iso()}`
"""
    text = replace_or_append_publish(read_text(prediction), section)
    write_text(prediction, text, force=True)

    if rel not in state.get("pending_retros", []):
        state.setdefault("pending_retros", []).append(rel)
    state.setdefault("published", []).append(
        {
            "prediction_file": rel,
            "platform": args.platform,
            "url": args.url,
            "published_at": now_iso(),
        }
    )
    state["last_published_at"] = now_iso()
    save_state(project, state)
    print(f"published: {rel}")
    return 0


def cmd_retro(args: argparse.Namespace) -> int:
    project = project_path(args.project)
    state = load_state(project)
    prediction = inside_project(project, args.prediction)
    if not prediction.exists():
        raise SystemExit(f"error: prediction not found: {prediction}")

    original = read_text(prediction)
    center = parse_predicted_center(original)
    signed_error = "n/a"
    direction = "on-target"
    if center and center != 0:
        pct = (args.views - center) / center * 100
        signed_error = f"{pct:+.1f}%"
        if pct > 25:
            direction = "high"
        elif pct < -25:
            direction = "low"

    section = render_template(
        "retro.md",
        {
            "RETRO_AT": now_iso(),
            "DATA_SOURCE": args.source,
            "VIEWS": args.views,
            "LIKES": args.likes,
            "COMMENTS": args.comments,
            "SHARES": args.shares,
            "PREDICTED_CENTER": center if center is not None else "unknown",
            "ACTUAL_RESULT": args.views,
            "SIGNED_ERROR": signed_error,
            "VALIDATED": args.validated or "TBD",
            "FALSIFIED": args.falsified or "TBD",
            "NOTES": args.notes or "TBD",
        },
    )

    updated = replace_or_append_retro(original, section, force=args.force)
    write_text(prediction, updated, force=True)

    rel = rel_to_project(project, prediction)
    retro_file = project / "retros" / prediction.name
    write_text(retro_file, section, force=args.force)

    state["calibration_samples"] = int(state.get("calibration_samples", 0)) + 1
    state["last_retro_at"] = now_iso()
    state["pending_retros"] = [x for x in state.get("pending_retros", []) if x != rel]
    errors = list(state.get("consecutive_directional_errors", []))
    errors.append(direction)
    state["consecutive_directional_errors"] = errors[-5:]
    save_state(project, state)

    print(f"retro appended: {rel}")
    print(f"signed_error: {signed_error}")
    return 0


def iter_prediction_files(project: Path) -> Iterable[Path]:
    pred_dir = project / "predictions"
    if not pred_dir.exists():
        return []
    return sorted(pred_dir.glob("*.md"))


@dataclass
class CurveRow:
    file: str
    predicted_center: float | None
    actual: float | None
    signed_error_pct: float | None


def collect_curve_rows(project: Path) -> list[CurveRow]:
    rows = []
    actual_re = re.compile(r"\*\*Actual Result\*\*:\s*`?([0-9]+(?:\.[0-9]+)?)`?")
    for path in iter_prediction_files(project):
        text = read_text(path)
        center = parse_predicted_center(text)
        match = actual_re.search(text)
        actual = float(match.group(1)) if match else None
        error = None
        if center and actual is not None:
            error = (actual - center) / center * 100
        rows.append(CurveRow(path.name, center, actual, error))
    return rows


def cmd_curve(args: argparse.Namespace) -> int:
    project = project_path(args.project)
    rows = collect_curve_rows(project)
    out = open(args.out, "w", newline="", encoding="utf-8") if args.out else sys.stdout
    try:
        writer = csv.writer(out)
        writer.writerow(["file", "predicted_center", "actual", "signed_error_pct"])
        for row in rows:
            writer.writerow(
                [
                    row.file,
                    row.predicted_center if row.predicted_center is not None else "",
                    row.actual if row.actual is not None else "",
                    f"{row.signed_error_pct:.1f}" if row.signed_error_pct is not None else "",
                ]
            )
    finally:
        if args.out:
            out.close()
    if args.out:
        print(f"curve csv written: {args.out}")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    project = project_path(args.project)
    state = load_state(project)
    prediction_files = list(iter_prediction_files(project))
    retro_done = sum(1 for p in prediction_files if prediction_has_completed_retro(read_text(p)))

    print(f"project: {project}")
    print(f"rubric_version: {state.get('rubric_version')}")
    print(f"calibration_samples: {state.get('calibration_samples', 0)}")
    print(f"predictions: {len(prediction_files)}")
    print(f"retros_completed: {retro_done}")
    print(f"pending_retros: {len(state.get('pending_retros', []))}")
    if state.get("pending_retros"):
        for item in state["pending_retros"]:
            print(f"  - {item}")
    print(f"last_script_file: {state.get('last_script_file')}")
    print(f"last_prediction_file: {state.get('last_prediction_file')}")
    print(f"last_published_at: {state.get('last_published_at')}")
    print(f"last_retro_at: {state.get('last_retro_at')}")
    return 0


SENSITIVE_VALUE_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|secret|token|cookie|session|password)[ \t]*[:=][ \t]*['\"]?[A-Za-z0-9_\-./+=]{12,}"),
    re.compile(r"(?i)authorization[ \t]*[:=][ \t]*['\"]?bearer[ \t]+[A-Za-z0-9_\-./+=]{12,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
]

PRIVATE_FILE_PATTERNS = [
    re.compile(r"(?i)\.env$"),
    re.compile(r"(?i)\.(db|sqlite|sqlite3)$"),
    re.compile(r"(?i)(cookies|session)"),
]

SKIP_DIRS = {".git", ".obsidian", "__pycache__", ".venv", "venv", ".content-os-cache"}


def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def read_maybe_text(path: Path) -> str | None:
    if path.stat().st_size > 1_000_000:
        return None
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None


def cmd_scan_public(args: argparse.Namespace) -> int:
    root = project_path(args.path)
    warnings: list[str] = []
    custom_terms = [term for term in (args.term or []) if term]

    for path in sorted(root.rglob("*")):
        if should_skip(path.relative_to(root)):
            continue
        if path.is_dir():
            continue
        rel = path.relative_to(root).as_posix()

        for pattern in PRIVATE_FILE_PATTERNS:
            if pattern.search(path.name) and path.name != ".env.example":
                warnings.append(f"{rel}: suspicious private file name")

        text = read_maybe_text(path)
        if text is None:
            suffix = path.suffix.lower()
            if suffix in {".png", ".jpg", ".jpeg", ".webp", ".pdf", ".zip"}:
                warnings.append(f"{rel}: binary asset; manually verify it is not private")
            continue

        for pattern in SENSITIVE_VALUE_PATTERNS:
            if pattern.search(text):
                warnings.append(f"{rel}: possible secret value")

        for match in re.finditer(r"https?://[^\s)>\"]+", text):
            url = match.group(0)
            if "example.com" not in url and "json-schema.org" not in url:
                warnings.append(f"{rel}: non-example URL {url}")

        for term in custom_terms:
            if term in text:
                warnings.append(f"{rel}: contains custom sensitive term {term!r}")

    if warnings:
        print("scan warnings:")
        for warning in warnings:
            print(f"  - {warning}")
        return 0 if args.warn_only else 1

    print("scan ok: no obvious secrets or private content found")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="content_os.py", description="Chuo's Content OS workflow CLI")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init", help="initialize a private content workspace")
    p.add_argument("project")
    p.add_argument("--default-platform", default=None)
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("new-script", help="create a draft script")
    p.add_argument("project")
    p.add_argument("title")
    p.add_argument("--form", default=None)
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_new_script)

    p = sub.add_parser("predict", help="write a blind prediction log")
    p.add_argument("project")
    p.add_argument("script")
    p.add_argument("--bucket", required=True)
    p.add_argument("--center", required=True, type=float)
    p.add_argument("--reason", required=True)
    p.add_argument("--scores", default="")
    p.add_argument("--summary", default="")
    p.add_argument("--p-lower", default="30%")
    p.add_argument("--p-expected", default="40%")
    p.add_argument("--p-higher", default="30%")
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_predict)

    p = sub.add_parser("publish", help="register a published piece")
    p.add_argument("project")
    p.add_argument("prediction")
    p.add_argument("--platform", required=True)
    p.add_argument("--url", required=True)
    p.set_defaults(func=cmd_publish)

    p = sub.add_parser("retro", help="append retrospective data")
    p.add_argument("project")
    p.add_argument("prediction")
    p.add_argument("--views", required=True, type=float)
    p.add_argument("--likes", default=0, type=float)
    p.add_argument("--comments", default=0, type=float)
    p.add_argument("--shares", default=0, type=float)
    p.add_argument("--source", default="manual")
    p.add_argument("--validated", default="")
    p.add_argument("--falsified", default="")
    p.add_argument("--notes", default="")
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_retro)

    p = sub.add_parser("status", help="show project status")
    p.add_argument("project")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("curve", help="emit prediction accuracy CSV")
    p.add_argument("project")
    p.add_argument("--out", default="")
    p.set_defaults(func=cmd_curve)

    p = sub.add_parser("scan-public", help="scan a public repo for likely private data")
    p.add_argument("path")
    p.add_argument("--term", action="append", help="custom sensitive term to search for")
    p.add_argument("--warn-only", action="store_true")
    p.set_defaults(func=cmd_scan_public)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
