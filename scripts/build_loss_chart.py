#!/usr/bin/env python3
"""Render a dependency-free SVG loss curve from a sanitized series CSV."""

from __future__ import annotations

import argparse
import csv
from html import escape
from pathlib import Path
from typing import Iterable


def load_series(path: Path) -> list[tuple[int, float]]:
    with path.open("r", encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    points = [(int(row["step"]), float(row["loss"])) for row in rows]
    if len(points) < 2:
        raise ValueError("At least two step/loss points are required")
    return sorted(points)


def render_loss_chart(
    points: Iterable[tuple[int, float]], title: str = "Training loss"
) -> str:
    values = list(points)
    if len(values) < 2:
        raise ValueError("At least two points are required")

    width, height = 960, 520
    left, right, top, bottom = 82, 30, 58, 68
    plot_width = width - left - right
    plot_height = height - top - bottom

    steps = [step for step, _ in values]
    losses = [loss for _, loss in values]
    min_step, max_step = min(steps), max(steps)
    min_loss, max_loss = min(losses), max(losses)
    if max_step == min_step:
        max_step += 1
    if max_loss == min_loss:
        max_loss += 1.0
    loss_padding = (max_loss - min_loss) * 0.06
    min_loss -= loss_padding
    max_loss += loss_padding

    def x(step: int) -> float:
        return left + (step - min_step) / (max_step - min_step) * plot_width

    def y(loss: float) -> float:
        return top + (max_loss - loss) / (max_loss - min_loss) * plot_height

    polyline = " ".join(f"{x(step):.2f},{y(loss):.2f}" for step, loss in values)
    grid: list[str] = []
    labels: list[str] = []
    for index in range(6):
        fraction = index / 5
        gx = left + fraction * plot_width
        gy = top + fraction * plot_height
        step_label = round(min_step + fraction * (max_step - min_step))
        loss_label = max_loss - fraction * (max_loss - min_loss)
        grid.append(
            f'<line x1="{gx:.2f}" y1="{top}" x2="{gx:.2f}" y2="{top + plot_height}" />'
        )
        grid.append(
            f'<line x1="{left}" y1="{gy:.2f}" x2="{left + plot_width}" y2="{gy:.2f}" />'
        )
        labels.append(
            f'<text x="{gx:.2f}" y="{height - 34}" text-anchor="middle">{step_label}</text>'
        )
        labels.append(
            f'<text x="{left - 12}" y="{gy + 5:.2f}" text-anchor="end">{loss_label:.3f}</text>'
        )

    return "\n".join(
        [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
            f"<title id=\"title\">{escape(title)}</title>",
            '<desc id="desc">Loss by optimization step from a sanitized training log.</desc>',
            "<style>",
            "  .bg{fill:#0d1117}.grid{stroke:#30363d;stroke-width:1}.axis{fill:#8b949e;font:13px system-ui,sans-serif}",
            "  .heading{fill:#f0f6fc;font:600 22px system-ui,sans-serif}.curve{fill:none;stroke:#58a6ff;stroke-width:2}",
            "</style>",
            f'<rect class="bg" width="{width}" height="{height}" rx="12"/>',
            f'<text class="heading" x="{left}" y="34">{escape(title)}</text>',
            f'<g class="grid">{"".join(grid)}</g>',
            f'<g class="axis">{"".join(labels)}</g>',
            f'<text class="axis" x="{left + plot_width / 2:.2f}" y="{height - 8}" text-anchor="middle">optimization step</text>',
            f'<text class="axis" transform="translate(18 {top + plot_height / 2:.2f}) rotate(-90)" text-anchor="middle">loss</text>',
            f'<polyline class="curve" points="{polyline}"/>',
            "</svg>",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("series", type=Path, help="CSV from parse_training_log.py")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--title", default="Training loss")
    args = parser.parse_args()

    rendered = render_loss_chart(load_series(args.series), title=args.title)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
