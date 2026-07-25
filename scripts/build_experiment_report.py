#!/usr/bin/env python3
"""Build the public historical-run table from experiments/registry.json."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "experiments" / "registry.json"
DEFAULT_OUTPUT = ROOT / "experiments" / "README.md"


def _show(value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, bool):
        return "yes" if value else "no"
    return str(value)


def _format_lr(value: Any) -> str:
    return f"{value:.0e}" if isinstance(value, (int, float)) else _show(value)


def render_registry(data: dict[str, Any]) -> str:
    audit = data["source_audit"]
    runs = data["runs"]
    lines = [
        "# Historical experiment registry",
        "",
        "> **Observational evidence, not a controlled ablation study.** The runs used different",
        "> datasets and multiple settings changed at once. They document real engineering history,",
        "> failures, and artifacts; they do not establish causal hyperparameter comparisons.",
        "",
        "This page is generated from [`registry.json`](registry.json) with",
        "[`scripts/build_experiment_report.py`](../scripts/build_experiment_report.py).",
        "Personal target names, prompts, raw paths, source images, weights, and optimizer states",
        "are intentionally excluded.",
        "",
        "## Local evidence audit",
        "",
        "| Evidence type | Count |",
        "|---|---:|",
        f"| Sanitized configuration records | {audit['configuration_files']} |",
        f"| Available local logs | {audit['log_files']} |",
        f"| Curated datasets | {audit['datasets']} |",
        f"| Image files | {audit['image_files']} |",
        f"| Caption files | {audit['caption_files']} |",
        f"| Matched image/caption pairs | {audit['matched_image_caption_pairs']} |",
        f"| Unmatched images / captions | {audit['unmatched_image_files']} / {audit['unmatched_caption_files']} |",
        f"| LoRA checkpoint files | {audit['checkpoint_files']} |",
        f"| Generated validation images | {audit['validation_images']} |",
        "",
        f"Audit date: `{audit['audited_at']}`. The counts describe local evidence; excluded",
        "artifacts are not distributed by this repository.",
        "",
        "## Runs",
        "",
        "| Run | Base | Status | Dataset | Steps | Rank | LR | Evidence |",
        "|---|---|---|---:|---:|---:|---:|---|",
    ]

    run_notes: list[str] = []
    for run in runs:
        config = run["config"]
        observed = run["observed"]
        evidence = ", ".join(run["evidence"])
        lines.append(
            "| `{id}` | `{base}` | `{status}` | {dataset} images ({matched} matched) | {steps} | "
            "{rank} | {lr} | {evidence} |".format(
                id=run["id"],
                base=run["base_model"].split("/")[-1],
                status=run["status"],
                dataset=config["dataset_images"],
                matched=config["matched_caption_pairs"],
                steps=config["steps"],
                rank=config["rank"],
                lr=_format_lr(config["learning_rate"]),
                evidence=evidence,
            )
        )
        if observed.get("note"):
            run_notes.append(f"- `{run['id']}`: {observed['note']}")

    lines.extend(
        [
            "",
            "### Evidence notes",
            "",
            *run_notes,
            "",
            "## Status definitions",
            "",
            "- `completed`: the log reaches the configured terminal step and a final checkpoint event exists.",
            "- `failed_oom`: the available log ends with a CUDA out-of-memory failure and no completion evidence.",
            "- `interrupted`: numbered checkpoints exist, but there is no final checkpoint or complete log.",
            "- `mixed_evidence`: artifacts and the available log appear to describe different attempts in the same run folder; no completion claim is made.",
            "",
            "## What can and cannot be concluded",
            "",
            "The registry supports the claims that local LoRA training was executed, checkpoints",
            "were produced, OOM failures were investigated, and one FLUX.1 run completed with",
            "a full log and validation samples. It does **not** support ranking learning rates,",
            "LoRA ranks, datasets, or FLUX versions against each other.",
            "",
            "A future controlled study should keep the dataset, seed, prompt suite, resolution,",
            "optimizer, and hardware fixed while changing one variable at a time. The planned",
            "protocol is documented in [the reproducibility guide](../docs/08-reproducibility.md).",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if the generated report differs from the checked-in file",
    )
    args = parser.parse_args()

    data = json.loads(args.registry.read_text(encoding="utf-8"))
    rendered = render_registry(data)

    if args.check:
        current = args.output.read_text(encoding="utf-8") if args.output.exists() else ""
        if current != rendered:
            print(f"{args.output} is out of date")
            return 1
        print(f"{args.output} is up to date")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
