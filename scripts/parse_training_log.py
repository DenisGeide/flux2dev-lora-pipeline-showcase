#!/usr/bin/env python3
"""Extract a small, path-free summary from an AI-Toolkit training log.

The parser intentionally emits metrics and event counts only. It never copies
raw log lines, local paths, prompts, trigger words, or checkpoint names into
the resulting JSON/Markdown report.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import statistics
from pathlib import Path
from typing import Any


ANSI_RE = re.compile(r"\x1b(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
PROGRESS_RE = re.compile(
    r"(?P<step>\d+)/(?P<total>\d+)\s+\["
    r"(?P<elapsed>\d+(?::\d+){1,2})<[^]]*?"
    r"(?P<seconds>\d+(?:\.\d+)?)s/it"
    r".*?lr:\s*(?P<lr>[+-]?\d+(?:\.\d+)?(?:e[+-]?\d+)?)"
    r"\s+loss:\s*(?P<loss>[+-]?\d+(?:\.\d+)?(?:e[+-]?\d+)?)",
    re.IGNORECASE,
)
CHECKPOINT_RE = re.compile(r"Saved checkpoint to\s+(.+?\.safetensors)", re.IGNORECASE)
NUMBERED_CHECKPOINT_RE = re.compile(r"_\d{9}\.safetensors$", re.IGNORECASE)
OOM_RE = re.compile(r"(?:CUDA\s+error:\s+out\s+of\s+memory|CUDA\s+out\s+of\s+memory|\bOOM\b)", re.IGNORECASE)


def _duration_seconds(value: str) -> int:
    parts = [int(part) for part in value.split(":")]
    if len(parts) == 2:
        minutes, seconds = parts
        return minutes * 60 + seconds
    if len(parts) == 3:
        hours, minutes, seconds = parts
        return hours * 3600 + minutes * 60 + seconds
    raise ValueError(f"Unsupported duration: {value}")


def _rounded(value: float | None, digits: int = 6) -> float | None:
    return round(value, digits) if value is not None else None


def extract_training_series(text: str) -> list[dict[str, Any]]:
    """Return one sanitized progress point per reported optimization step."""

    clean = ANSI_RE.sub("", text).replace("\r", "\n")
    progress_by_step: dict[int, dict[str, Any]] = {}
    for line in clean.splitlines():
        match = PROGRESS_RE.search(line)
        if not match:
            continue
        step = int(match.group("step"))
        progress_by_step[step] = {
            "step": step,
            "target_steps": int(match.group("total")),
            "elapsed_seconds": _duration_seconds(match.group("elapsed")),
            "seconds_per_iteration": float(match.group("seconds")),
            "learning_rate": float(match.group("lr")),
            "loss": float(match.group("loss")),
        }
    return [progress_by_step[key] for key in sorted(progress_by_step)]


def parse_training_log(text: str, run_id: str = "local-run") -> dict[str, Any]:
    """Parse AI-Toolkit console output into a sanitized summary."""

    clean = ANSI_RE.sub("", text).replace("\r", "\n")
    points = extract_training_series(clean)
    checkpoint_files: set[str] = set()
    final_checkpoint_files: set[str] = set()
    oom_positions: list[int] = []
    final_checkpoint_positions: list[int] = []

    for position, line in enumerate(clean.splitlines()):
        checkpoint = CHECKPOINT_RE.search(line)
        if checkpoint:
            filename = re.split(r"[/\\]", checkpoint.group(1).strip())[-1]
            checkpoint_files.add(filename)
            if not NUMBERED_CHECKPOINT_RE.search(filename):
                final_checkpoint_files.add(filename)
                final_checkpoint_positions.append(position)

        if OOM_RE.search(line):
            oom_positions.append(position)

    max_step = points[-1]["step"] if points else None
    target_steps = max((point["target_steps"] for point in points), default=None)
    completion_evidence = bool(
        final_checkpoint_positions
        and target_steps is not None
        and max_step is not None
        and max_step >= target_steps - 1
    )

    if completion_evidence and (
        not oom_positions or final_checkpoint_positions[-1] > oom_positions[-1]
    ):
        status = "completed"
    elif final_checkpoint_files:
        # A final-looking filename without terminal progress is conflicting
        # evidence, not proof of completion. It may belong to a different
        # attempt in a reused output directory.
        status = "mixed_evidence"
    elif oom_positions:
        status = "failed_oom"
    elif points or checkpoint_files:
        status = "incomplete"
    else:
        status = "unknown"

    losses = [point["loss"] for point in points]
    speeds = [point["seconds_per_iteration"] for point in points]
    last_point = points[-1] if points else None

    return {
        "schema_version": "1.0",
        "run_id": run_id,
        "status": status,
        "progress": {
            "unique_reported_steps": len(points),
            "max_reported_step": max_step,
            "target_steps": target_steps,
            "progress_percent": (
                _rounded(100 * (max_step + 1) / target_steps, 2)
                if max_step is not None and target_steps
                else None
            ),
            "elapsed_seconds": last_point["elapsed_seconds"] if last_point else None,
            "median_seconds_per_iteration": (
                _rounded(statistics.median(speeds), 3) if speeds else None
            ),
        },
        "optimization": {
            "last_reported_learning_rate": (
                last_point["learning_rate"] if last_point else None
            ),
            "last_reported_loss": last_point["loss"] if last_point else None,
            "minimum_reported_loss": _rounded(min(losses)) if losses else None,
            "mean_reported_loss": (
                _rounded(statistics.fmean(losses)) if losses else None
            ),
        },
        "events": {
            "checkpoint_events": len(checkpoint_files),
            "final_checkpoint_events": len(final_checkpoint_files),
            "cuda_oom_detected": bool(oom_positions),
        },
        "privacy": {
            "raw_lines_included": False,
            "paths_included": False,
            "prompts_included": False,
        },
    }


def render_markdown(summary: dict[str, Any]) -> str:
    progress = summary["progress"]
    optimization = summary["optimization"]
    events = summary["events"]

    def show(value: Any) -> str:
        return "n/a" if value is None else str(value)

    return "\n".join(
        [
            f"# Training log summary: `{summary['run_id']}`",
            "",
            "> Generated from a local log. Raw lines, paths, prompts, and trigger words are excluded.",
            "",
            "| Field | Value |",
            "|---|---:|",
            f"| Status | `{summary['status']}` |",
            f"| Highest reported step | {show(progress['max_reported_step'])} |",
            f"| Target steps | {show(progress['target_steps'])} |",
            f"| Progress | {show(progress['progress_percent'])}% |",
            f"| Elapsed seconds | {show(progress['elapsed_seconds'])} |",
            f"| Median seconds/iteration | {show(progress['median_seconds_per_iteration'])} |",
            f"| Last reported loss | {show(optimization['last_reported_loss'])} |",
            f"| Minimum reported loss | {show(optimization['minimum_reported_loss'])} |",
            f"| Unique checkpoint events | {events['checkpoint_events']} |",
            f"| Unique final checkpoint events | {events['final_checkpoint_events']} |",
            f"| CUDA OOM detected | {str(events['cuda_oom_detected']).lower()} |",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log", type=Path, help="Path to an AI-Toolkit text log")
    parser.add_argument("--run-id", default="local-run", help="Public/sanitized run ID")
    parser.add_argument("--output", type=Path, help="Write the JSON summary here")
    parser.add_argument(
        "--series-output",
        type=Path,
        help="Optionally write deduplicated step/loss/speed data as CSV",
    )
    parser.add_argument(
        "--markdown-output", type=Path, help="Optionally write a Markdown summary"
    )
    args = parser.parse_args()

    raw_text = args.log.read_text(encoding="utf-8", errors="replace")
    summary = parse_training_log(raw_text, run_id=args.run_id)
    payload = json.dumps(summary, indent=2, sort_keys=True) + "\n"

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")

    if args.markdown_output:
        args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_output.write_text(render_markdown(summary), encoding="utf-8")

    if args.series_output:
        series = extract_training_series(raw_text)
        args.series_output.parent.mkdir(parents=True, exist_ok=True)
        with args.series_output.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(
                stream,
                fieldnames=(
                    "step",
                    "target_steps",
                    "elapsed_seconds",
                    "seconds_per_iteration",
                    "learning_rate",
                    "loss",
                ),
            )
            writer.writeheader()
            writer.writerows(series)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
