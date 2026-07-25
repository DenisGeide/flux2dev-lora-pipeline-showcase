# Model and adapter card

## Artifact

This repository documents LoRA adapter training for FLUX.1-dev and FLUX.2-dev.
It does not distribute a base model or LoRA weights.

## Components

| Component | Role | Distributed here |
|---|---|---|
| FLUX.1-dev / FLUX.2-dev | third-party base model | no |
| `ostris/ai-toolkit` | third-party training implementation | no |
| ComfyUI | third-party inference workflow runtime | no |
| sanitized configs | reproducibility reference | yes |
| experiment registry and report tools | public evidence layer | yes |
| historical LoRA checkpoints | private experiment artifacts | no |

## Intended use

- education about local LoRA experiment operation;
- reproducible configuration and dataset-manifest patterns;
- analysis of OOM and interrupted runs;
- fixed-prompt comparison of checkpoints;
- preparation for a controlled study.

## Out of scope

- impersonation or deceptive identity generation;
- training on images without a lawful basis or consent;
- presenting the included config as universally optimal;
- claiming the third-party AI-Toolkit trainer as original project code;
- claiming historical runs form a controlled ablation.

## Evidence

The local audit found seven configuration records, four logs, 23 checkpoint
files, and 56 validation images. One FLUX.1 run has an unambiguous completion
log and final checkpoint. FLUX.2 evidence includes partial checkpoints, OOM
failures, and one folder with mixed attempt evidence. Exact records are in the
[experiment registry](../experiments/README.md).

## Evaluation

Historical visual assessment considered prompt adherence, subject consistency,
detail retention, texture, and artifacts. It was not blinded or statistically
controlled, and those generated images are not distributed. Future evaluation
should use:

- fixed prompts and seeds;
- held-out compositions;
- checkpoint-by-checkpoint grids;
- blinded human scoring with at least two reviewers;
- explicit artifact/failure categories;
- wall time and peak VRAM alongside visual quality.

## Limitations

- The public SVGs are illustrative diagrams, not qualitative model examples.
- Historical generated images remain local because release rights and exact
  run-to-image provenance were not retained at the required level.
- Training loss is not a perceptual quality metric.
- Exact reproduction depends on model access, third-party versions, hardware,
  and non-deterministic GPU behavior.
- Model and dataset licenses apply independently from this repository's MIT license.
