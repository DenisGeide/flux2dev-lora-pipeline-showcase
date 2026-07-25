#!/usr/bin/env python3
"""Validate a public LoRA dataset manifest without loading image content."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def _safe_relative_path(value: Any, field: str, errors: list[str]) -> Path | None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{field} must be a non-empty string")
        return None

    normalized = value.replace("\\", "/")
    pure = PurePosixPath(normalized)
    if pure.is_absolute() or ".." in pure.parts or ":" in normalized:
        errors.append(f"{field} must be a safe relative path")
        return None
    return Path(*pure.parts)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_manifest(
    manifest: dict[str, Any], dataset_root: Path | None = None
) -> list[str]:
    errors: list[str] = []
    allowed_top_level = {
        "$schema",
        "schema_version",
        "dataset_id",
        "version",
        "description",
        "license",
        "rights",
        "caption_strategy",
        "items",
    }
    required_top_level = {
        "schema_version",
        "dataset_id",
        "version",
        "license",
        "rights",
        "items",
    }
    missing = sorted(required_top_level - manifest.keys())
    if missing:
        errors.append(f"missing top-level fields: {', '.join(missing)}")
    unexpected = sorted(manifest.keys() - allowed_top_level)
    if unexpected:
        errors.append(f"unexpected top-level fields: {', '.join(unexpected)}")

    if manifest.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")
    for field in ("dataset_id", "version", "license"):
        if not isinstance(manifest.get(field), str) or not manifest[field].strip():
            errors.append(f"{field} must be a non-empty string")

    rights = manifest.get("rights")
    if not isinstance(rights, dict):
        errors.append("rights must be an object")
    else:
        allowed_rights = {
            "basis",
            "public_release_approved",
            "contains_personal_data",
            "notes",
        }
        unexpected_rights = sorted(rights.keys() - allowed_rights)
        if unexpected_rights:
            errors.append(
                "unexpected rights fields: " + ", ".join(unexpected_rights)
            )
        if rights.get("public_release_approved") is not True:
            errors.append("rights.public_release_approved must be true")
        if rights.get("contains_personal_data") is not False:
            errors.append("rights.contains_personal_data must be false")
        if (
            not isinstance(rights.get("basis"), str)
            or not rights["basis"].strip()
        ):
            errors.append("rights.basis must explain the ownership/license basis")

    items = manifest.get("items")
    if not isinstance(items, list) or not items:
        errors.append("items must be a non-empty array")
        return errors

    seen_ids: set[str] = set()
    allowed_item_fields = {
        "id",
        "image",
        "caption",
        "split",
        "width",
        "height",
        "sha256",
        "source",
        "license",
    }
    for index, item in enumerate(items):
        prefix = f"items[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue

        unexpected_item_fields = sorted(item.keys() - allowed_item_fields)
        if unexpected_item_fields:
            errors.append(
                f"{prefix} has unexpected fields: "
                + ", ".join(unexpected_item_fields)
            )

        item_id = item.get("id")
        if not isinstance(item_id, str) or not item_id:
            errors.append(f"{prefix}.id must be a non-empty string")
        elif item_id in seen_ids:
            errors.append(f"{prefix}.id is duplicated: {item_id}")
        else:
            seen_ids.add(item_id)

        image_rel = _safe_relative_path(item.get("image"), f"{prefix}.image", errors)
        caption_rel = _safe_relative_path(
            item.get("caption"), f"{prefix}.caption", errors
        )
        if image_rel and image_rel.suffix.lower() not in IMAGE_EXTENSIONS:
            errors.append(f"{prefix}.image has an unsupported extension")
        if caption_rel and caption_rel.suffix.lower() != ".txt":
            errors.append(f"{prefix}.caption must point to a .txt sidecar")

        split = item.get("split")
        if split not in {"train", "validation", "test"}:
            errors.append(f"{prefix}.split must be train, validation, or test")

        expected_hash = item.get("sha256")
        if expected_hash is not None and (
            not isinstance(expected_hash, str)
            or len(expected_hash) != 64
            or any(char not in "0123456789abcdefABCDEF" for char in expected_hash)
        ):
            errors.append(f"{prefix}.sha256 must be a 64-character hex digest")

        if dataset_root is not None:
            for label, relative in (("image", image_rel), ("caption", caption_rel)):
                if relative is None:
                    continue
                candidate = dataset_root / relative
                if not candidate.is_file():
                    errors.append(f"{prefix}.{label} does not exist under dataset root")
            if image_rel and expected_hash:
                image_path = dataset_root / image_rel
                if image_path.is_file() and _sha256(image_path) != expected_hash.lower():
                    errors.append(f"{prefix}.sha256 does not match the image")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument(
        "--dataset-root",
        type=Path,
        help="Also verify that referenced files exist and hashes match",
    )
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    errors = validate_manifest(manifest, args.dataset_root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: {args.manifest} ({len(manifest['items'])} items)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
