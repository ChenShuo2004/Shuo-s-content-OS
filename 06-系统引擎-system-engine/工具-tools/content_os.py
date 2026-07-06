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
from urllib.parse import urlparse


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


VERSION = "0.1.0"
STATE_FILE = ".content-os-state.json"
ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = ROOT / "模板-templates"

ENTRY_DIR = Path("00-项目入口-entry")
PRODUCT_DIR = Path("01-产品本体-product-core")
MARKET_DIR = Path("02-市场与竞品-market-research")
CONTENT_SALES_DIR = Path("03-内容与销售-content-sales")
PIPELINE_DIR = Path("04-创作流水线-creation-pipeline")
CALIBRATION_DIR = Path("05-校准与复盘-calibration-retro")
ENGINE_DIR = Path("06-系统引擎-system-engine")
RAW_DIR = Path("99-原始资料-raw-materials")

SCRIPTS_DIR = PIPELINE_DIR / "草稿-scripts"
SAMPLES_DIR = PIPELINE_DIR / "样本-samples"
VIDEOS_DIR = PIPELINE_DIR / "已拍视频-videos"
PREDICTIONS_DIR = CALIBRATION_DIR / "评分预测系统-scoring-prediction" / "预测日志-predictions"
RETROS_DIR = CALIBRATION_DIR / "复盘记录-retros"
CANDIDATES_FILE = PIPELINE_DIR / "candidates.md"


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
    direct = (project / raw).resolve()
    if direct.exists():
        return direct
    if raw.parts:
        head = raw.parts[0]
        tail = Path(*raw.parts[1:]) if len(raw.parts) > 1 else Path()
        if head == "scripts":
            return (project / SCRIPTS_DIR / tail).resolve()
        if head == "predictions":
            return (project / PREDICTIONS_DIR / tail).resolve()
        if head == "retros":
            return (project / RETROS_DIR / tail).resolve()
    return direct


def rel_to_project(project: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(project.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def command_alias(project: Path, path: Path) -> str:
    rel = rel_to_project(project, path)
    prefix_map = {
        SCRIPTS_DIR.as_posix(): "scripts",
        PREDICTIONS_DIR.as_posix(): "predictions",
        RETROS_DIR.as_posix(): "retros",
    }
    for long_prefix, short_prefix in prefix_map.items():
        if rel.startswith(long_prefix + "/"):
            return short_prefix + rel[len(long_prefix) :]
    return rel


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

    folders = (
        ENTRY_DIR,
        ENTRY_DIR / "飞书与仪表盘-feishu-dashboards",
        PRODUCT_DIR,
        MARKET_DIR,
        CONTENT_SALES_DIR,
        CONTENT_SALES_DIR / "平台模板-platform-template" / "00-平台总览",
        CONTENT_SALES_DIR / "平台模板-platform-template" / "01-账号定位",
        CONTENT_SALES_DIR / "平台模板-platform-template" / "02-发布清单",
        CONTENT_SALES_DIR / "平台模板-platform-template" / "03-复盘数据",
        CONTENT_SALES_DIR / "平台模板-platform-template" / "04-策略素材",
        CONTENT_SALES_DIR / "平台模板-platform-template" / "05-配图库",
        CONTENT_SALES_DIR / "平台模板-platform-template" / "06-视觉资产",
        CONTENT_SALES_DIR / "平台模板-platform-template" / "07-对标账号",
        CONTENT_SALES_DIR / "平台模板-platform-template" / "08-文章库",
        SCRIPTS_DIR,
        SAMPLES_DIR,
        VIDEOS_DIR,
        CALIBRATION_DIR,
        CALIBRATION_DIR / "初始评分表-starter-rubrics",
        CALIBRATION_DIR / "评分预测系统-scoring-prediction",
        PREDICTIONS_DIR,
        RETROS_DIR,
        ENGINE_DIR,
        ENGINE_DIR / "共享规范-shared-references",
        ENGINE_DIR / "工具-tools",
        ENGINE_DIR / "模板-templates",
        RAW_DIR,
    )
    for folder in folders:
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
        "00-项目入口-entry/WORKFLOW.md": ("project/WORKFLOW.md", {}),
        "00-项目入口-entry/STATUS.md": ("project/STATUS.md", {}),
        "05-校准与复盘-calibration-retro/rubric_notes.md": ("project/rubric.md", {}),
        "05-校准与复盘-calibration-retro/rubric-memo.md": ("project/rubric-memo.md", {}),
        "05-校准与复盘-calibration-retro/audience.md": ("project/audience.md", {}),
        "05-校准与复盘-calibration-retro/benchmark.md": ("project/benchmark.md", {}),
        "05-校准与复盘-calibration-retro/script_patterns.md": ("project/script_patterns.md", {}),
        CANDIDATES_FILE.as_posix(): ("project/candidates.md", {}),
        STATE_FILE: ("state.json", mapping),
    }

    for dest_name, (template_name, extra) in files.items():
        dest = project / dest_name
        text = render_template(template_name, {**mapping, **extra})
        if write_text(dest, text, force=args.force):
            created.append(dest_name)
        else:
            skipped.append(dest_name)

    print(f"已初始化: {project}")
    if created:
        print("已创建:")
        for item in created:
            print(f"  {item}")
    if skipped:
        print("已存在，跳过:")
        for item in skipped:
            print(f"  {item}")
    return 0


def cmd_new_script(args: argparse.Namespace) -> int:
    project = project_path(args.project)
    state = load_state(project)
    content_id = sha12(f"{args.title}|{now_iso()}")
    filename = f"{today()}_{content_id}_{slugify(args.title)}.md"
    dest = project / SCRIPTS_DIR / filename

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
        raise SystemExit(f"error: 文件已存在: {dest}")

    state["last_script_file"] = rel_to_project(project, dest)
    save_state(project, state)
    print(f"实际路径: {rel_to_project(project, dest)}")
    print(command_alias(project, dest))
    return 0


def cmd_predict(args: argparse.Namespace) -> int:
    project = project_path(args.project)
    state = load_state(project)
    script = inside_project(project, args.script)
    if not script.exists():
        raise SystemExit(f"error: 找不到草稿: {script}")

    script_text = read_text(script)
    title = first_heading(script_text, script.stem)
    content_id = content_id_from_script(script, script_text)
    dest = project / PREDICTIONS_DIR / script.name

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
        raise SystemExit(f"error: 预测日志已存在: {dest}")

    state["last_prediction_file"] = rel_to_project(project, dest)
    save_state(project, state)
    print(f"实际路径: {rel_to_project(project, dest)}")
    print(command_alias(project, dest))
    return 0


def cmd_publish(args: argparse.Namespace) -> int:
    project = project_path(args.project)
    state = load_state(project)
    prediction = inside_project(project, args.prediction)
    if not prediction.exists():
        raise SystemExit(f"error: 找不到预测日志: {prediction}")

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
    print(f"已登记发布: {rel}")
    return 0


def cmd_retro(args: argparse.Namespace) -> int:
    project = project_path(args.project)
    state = load_state(project)
    prediction = inside_project(project, args.prediction)
    if not prediction.exists():
        raise SystemExit(f"error: 找不到预测日志: {prediction}")

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
    retro_file = project / RETROS_DIR / prediction.name
    write_text(retro_file, section, force=args.force)

    state["calibration_samples"] = int(state.get("calibration_samples", 0)) + 1
    state["last_retro_at"] = now_iso()
    state["pending_retros"] = [x for x in state.get("pending_retros", []) if x != rel]
    errors = list(state.get("consecutive_directional_errors", []))
    errors.append(direction)
    state["consecutive_directional_errors"] = errors[-5:]
    save_state(project, state)

    print(f"已追加复盘: {rel}")
    print(f"预测偏差: {signed_error}")
    return 0


def iter_prediction_files(project: Path) -> Iterable[Path]:
    pred_dir = project / PREDICTIONS_DIR
    if not pred_dir.exists():
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
        print(f"预测曲线 CSV 已写入: {args.out}")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    project = project_path(args.project)
    state = load_state(project)
    prediction_files = list(iter_prediction_files(project))
    retro_done = sum(1 for p in prediction_files if prediction_has_completed_retro(read_text(p)))

    print(f"项目: {project}")
    print(f"rubric_version: {state.get('rubric_version')}")
    print(f"校准样本数: {state.get('calibration_samples', 0)}")
    print(f"预测日志数: {len(prediction_files)}")
    print(f"已完成复盘: {retro_done}")
    print(f"待复盘: {len(state.get('pending_retros', []))}")
    if state.get("pending_retros"):
        for item in state["pending_retros"]:
            print(f"  - {item}")
    print(f"最近草稿: {state.get('last_script_file')}")
    print(f"最近预测: {state.get('last_prediction_file')}")
    print(f"最近发布: {state.get('last_published_at')}")
    print(f"最近复盘: {state.get('last_retro_at')}")
    return 0


SENSITIVE_ASSIGNMENT = re.compile(
    r"(?i)^\s*([A-Za-z0-9_.-]*(?:api[_-]?key|secret|token|cookie|session|password)[A-Za-z0-9_.-]*)"
    r"\s*[:=]\s*(.+?)\s*(?:#.*)?$"
)
SENSITIVE_INLINE_PATTERNS = [
    re.compile(r"(?i)authorization[ \t]*[:=][ \t]*['\"]?bearer[ \t]+[A-Za-z0-9_\-./+=]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
]

PRIVATE_FILE_PATTERNS = [
    re.compile(r"(?i)\.env$"),
    re.compile(r"(?i)\.(db|sqlite|sqlite3)$"),
    re.compile(r"(?i)(cookies|session)"),
]

SKIP_DIRS = {".git", ".obsidian", "__pycache__", ".venv", "venv", ".content-os-cache"}

PRIVATE_FILE_NAME_ALLOWLIST = {
    "session-start.json",
    "session-start.sh",
}

DEFAULT_PUBLIC_URL_DOMAINS = {
    "example.com",
    "json-schema.org",
    "github.com",
    "huggingface.co",
    "news.ycombinator.com",
    "api.bilibili.com",
    "www.bilibili.com",
    "b23.tv",
    "creator.douyin.com",
    "www.douyin.com",
    "v.douyin.com",
    "creator.xiaohongshu.com",
    "www.xiaohongshu.com",
    "xhslink.com",
    "www.linkedin.com",
    "s.weibo.com",
    "weibo.com",
    "www.zhihu.com",
    "aihot.virxact.com",
}


def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def read_maybe_text(path: Path) -> str | None:
    if path.stat().st_size > 1_000_000:
        return None
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None


def is_secret_assignment(line: str) -> bool:
    match = SENSITIVE_ASSIGNMENT.match(line)
    if not match:
        return False
    value = match.group(2).strip().rstrip(",")
    value = value.strip("\"'")

    if not value or value in {"...", "<redacted>", "REDACTED", "CHANGE_ME", "your-token-here"}:
        return False
    if value.startswith(("{", "$", "%", "os.", "env.", "Path(")):
        return False
    if any(ch in value for ch in "{}()<>"):
        return False
    return bool(re.fullmatch(r"[A-Za-z0-9_\-./+=]{20,}", value))


def is_public_url_allowed(url: str, allow_domains: set[str], strict_urls: bool) -> bool:
    if strict_urls:
        return "example.com" in url or "json-schema.org" in url
    if any(marker in url for marker in ("...", "<", ">", "{", "}")):
        return True
    host = urlparse(url).netloc.lower()
    if not host:
        return True
    return host in allow_domains or any(host.endswith("." + domain) for domain in allow_domains)


def cmd_scan_public(args: argparse.Namespace) -> int:
    root = project_path(args.path)
    warnings: list[str] = []
    custom_terms = [term for term in (args.term or []) if term]
    allow_domains = set(DEFAULT_PUBLIC_URL_DOMAINS)
    allow_domains.update(domain.lower() for domain in (args.allow_url_domain or []) if domain)

    for path in sorted(root.rglob("*")):
        if should_skip(path.relative_to(root)):
            continue
        if path.is_dir():
            continue
        rel = path.relative_to(root).as_posix()

        for pattern in PRIVATE_FILE_PATTERNS:
            if path.name in PRIVATE_FILE_NAME_ALLOWLIST:
                continue
            if pattern.search(path.name) and path.name != ".env.example":
                warnings.append(f"{rel}: suspicious private file name")

        text = read_maybe_text(path)
        if text is None:
            suffix = path.suffix.lower()
            if suffix in {".png", ".jpg", ".jpeg", ".webp", ".pdf", ".zip"}:
                warnings.append(f"{rel}: binary asset; manually verify it is not private")
            continue

        for pattern in SENSITIVE_INLINE_PATTERNS:
            if pattern.search(text):
                warnings.append(f"{rel}: possible secret value")
        for line_no, line in enumerate(text.splitlines(), start=1):
            if is_secret_assignment(line):
                warnings.append(f"{rel}:{line_no}: possible secret value")

        for match in re.finditer(r"https?://[^\s)>\"]+", text):
            url = match.group(0)
            if not is_public_url_allowed(url, allow_domains, args.strict_urls):
                warnings.append(f"{rel}: non-example URL {url}")

        for term in custom_terms:
            if term in text:
                warnings.append(f"{rel}: contains custom sensitive term {term!r}")

    if warnings:
        print("扫描警告:")
        for warning in warnings:
            print(f"  - {warning}")
        return 0 if args.warn_only else 1

    print("扫描通过: 未发现明显密钥或私有内容")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="content_os.py", description="绰的内容操作系统 CLI")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init", help="初始化一个私有内容工作区")
    p.add_argument("project")
    p.add_argument("--default-platform", default=None)
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("new-script", help="创建一篇草稿")
    p.add_argument("project")
    p.add_argument("title")
    p.add_argument("--form", default=None)
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_new_script)

    p = sub.add_parser("predict", help="写一份盲预测日志")
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

    p = sub.add_parser("publish", help="登记已发布内容")
    p.add_argument("project")
    p.add_argument("prediction")
    p.add_argument("--platform", required=True)
    p.add_argument("--url", required=True)
    p.set_defaults(func=cmd_publish)

    p = sub.add_parser("retro", help="追加复盘数据")
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

    p = sub.add_parser("status", help="查看项目状态")
    p.add_argument("project")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("curve", help="输出预测偏差 CSV")
    p.add_argument("project")
    p.add_argument("--out", default="")
    p.set_defaults(func=cmd_curve)

    p = sub.add_parser("scan-public", help="扫描公开仓库里的疑似隐私内容")
    p.add_argument("path")
    p.add_argument("--term", action="append", help="custom sensitive term to search for")
    p.add_argument("--allow-url-domain", action="append", help="public URL domain allowed in docs or adapters")
    p.add_argument("--strict-urls", action="store_true", help="flag every non-example URL")
    p.add_argument("--warn-only", action="store_true")
    p.set_defaults(func=cmd_scan_public)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
