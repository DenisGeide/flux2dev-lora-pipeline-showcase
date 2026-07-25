# Historical experiment registry

> **Observational evidence, not a controlled ablation study.** The runs used different
> datasets and multiple settings changed at once. They document real engineering history,
> failures, and artifacts; they do not establish causal hyperparameter comparisons.

This page is generated from [`registry.json`](registry.json) with
[`scripts/build_experiment_report.py`](../scripts/build_experiment_report.py).
Personal target names, prompts, raw paths, source images, weights, and optimizer states
are intentionally excluded.

## Local evidence audit

| Evidence type | Count |
|---|---:|
| Sanitized configuration records | 7 |
| Available local logs | 4 |
| Curated datasets | 4 |
| Image files | 98 |
| Caption files | 98 |
| Matched image/caption pairs | 97 |
| Unmatched images / captions | 1 / 1 |
| LoRA checkpoint files | 23 |
| Generated validation images | 56 |

Audit date: `2026-07-25`. The counts describe local evidence; excluded
artifacts are not distributed by this repository.

## Runs

| Run | Base | Status | Dataset | Steps | Rank | LR | Evidence |
|---|---|---|---:|---:|---:|---:|---|
| `hist-flux1-001` | `FLUX.1-dev` | `completed` | 32 images (31 matched) | 2250 | 32 | 4e-04 | full local log, final checkpoint, 56 validation images |
| `hist-flux2-002` | `FLUX.2-dev` | `mixed_evidence` | 32 images (31 matched) | 1800 | 16 | 1e-04 | mixed local artifacts, OOM log, final adapter file |
| `hist-flux2-003` | `FLUX.2-dev` | `interrupted` | 34 images (34 matched) | 3000 | 32 | 5e-05 | sanitized config, numbered checkpoints |
| `hist-flux2-004` | `FLUX.2-dev` | `interrupted` | 16 images (16 matched) | 1000 | 16 | 1e-04 | sanitized config, numbered checkpoints |
| `hist-flux2-005` | `FLUX.2-dev` | `interrupted` | 16 images (16 matched) | 1200 | 16 | 1e-04 | sanitized config, numbered checkpoints |
| `hist-flux2-006` | `FLUX.2-dev` | `failed_oom` | 32 images (31 matched) | 1800 | 16 | 1e-04 | full local OOM log, sanitized config |
| `hist-flux2-007` | `FLUX.2-dev` | `failed_oom` | 32 images (31 matched) | 3000 | 32 | 1e-04 | full local OOM log, sanitized config |

### Evidence notes

- `hist-flux1-001`: The progress log reaches 2249/2250 (zero-indexed display), then records four validation generations and a final checkpoint. This is the only locally audited run with unambiguous completion evidence.
- `hist-flux2-002`: A final adapter artifact and numbered checkpoints exist, while the currently available log records an OOM during a separate/retry model-load attempt. The evidence cannot safely be merged into a completion claim.
- `hist-flux2-003`: Four numbered checkpoints are present through step 2000 of 3000, but no log or final adapter artifact remains. The stop reason is unknown.
- `hist-flux2-004`: Numbered checkpoints are present through step 800 of 1000; no final adapter artifact or complete log remains.
- `hist-flux2-005`: Numbered checkpoints are present through step 1000 of 1200; no final adapter artifact or complete log remains.
- `hist-flux2-006`: The model and VAE loaded, then CUDA OOM occurred during model preparation before a training step was reported.
- `hist-flux2-007`: CUDA OOM occurred while quantizing transformer blocks, before the first training step.

## Status definitions

- `completed`: the log reaches the configured terminal step and a final checkpoint event exists.
- `failed_oom`: the available log ends with a CUDA out-of-memory failure and no completion evidence.
- `interrupted`: numbered checkpoints exist, but there is no final checkpoint or complete log.
- `mixed_evidence`: artifacts and the available log appear to describe different attempts in the same run folder; no completion claim is made.

## What can and cannot be concluded

The registry supports the claims that local LoRA training was executed, checkpoints
were produced, OOM failures were investigated, and one FLUX.1 run completed with
a full log and validation samples. It does **not** support ranking learning rates,
LoRA ranks, datasets, or FLUX versions against each other.

A future controlled study should keep the dataset, seed, prompt suite, resolution,
optimizer, and hardware fixed while changing one variable at a time. The planned
protocol is documented in [the reproducibility guide](../docs/08-reproducibility.md).
