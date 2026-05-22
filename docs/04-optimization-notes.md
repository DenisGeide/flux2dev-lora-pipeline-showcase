# Optimization Notes

This document explains the main optimization work done around FLUX2DEV inference and LoRA training.

The main problem was memory pressure. Default local configurations were not stable enough for heavier FLUX2DEV workloads, so the inference workflow and training setup had to be manually tuned.

## Main Problems

| Problem | What Happened | Impact |
|---|---|---|
| VRAM pressure | The workflow consumed too much GPU memory under heavier settings | OOM/crash risk |
| OOM errors | Runs failed during generation or training | Unstable workflow |
| Slow iteration | Failed runs increased experiment time | Longer training/debug cycle |
| Memory fragmentation | Long sessions became less predictable | Random crashes |
| Output instability | Some settings produced artifacts or weaker details | Lower result quality |

## Engineering Challenges Summary

This project is best understood as an engineering/debugging case study, not just an image generation experiment.

| Challenge | Practical Meaning |
|---|---|
| CUDA/OOM crashes | The system could fail during heavier local runs |
| VRAM pressure | Local memory had to be managed carefully |
| Training instability | LoRA training needed a more stable config |
| Offloading bottlenecks | Moving work between VRAM/RAM can help but may slow iteration |
| Sampler instability | Some sampler/guidance combinations produced weaker outputs |
| Dataset sensitivity | Small datasets require careful cleanup and testing |

## Main Optimization Areas

| Area | What Was Tuned |
|---|---|
| VRAM/RAM balancing | Adjusted which parts stayed on GPU and which were offloaded |
| Offloading | Reduced pressure from secondary nodes |
| Sampler chain | Tuned sampler behavior for stable output |
| Guidance/CFG | Tuned guidance to balance detail and stability |
| Sigma/noise behavior | Adjusted noise behavior through scheduler/sampler setup |
| Training config | Stabilized AI-Toolkit training under memory pressure |
| FP8 usage | Used on the LoRA/training side where applicable |

## Why There Is No Single Universal Config

The exact low-level values changed during experiments.

For FLUX2DEV LoRA training, the "right" settings depend on:

- GPU VRAM;
- system RAM;
- dataset size;
- caption/trigger-word quality;
- target style or subject;
- resolution;
- sampler/guidance behavior;
- how aggressively the workflow offloads model parts.

Because of that, this repository presents the config as a working reference and explains the tuning strategy instead of claiming that one set of numbers is optimal for every setup.

## Memory Strategy

The goal was to keep the pipeline usable on a local workstation rather than relying on cloud GPU servers.

The workflow was tuned around:

- reducing unnecessary VRAM pressure;
- using system RAM when useful;
- keeping core model operations stable;
- avoiding repeated OOM crashes;
- making experiments repeatable.

## FP8 Note

In this project, FP8 was used on the LoRA/training side where applicable.

Important distinction:

- regular generation is not described as fully FP8;
- training/LoRA optimization used FP8-related settings where they helped reduce memory pressure;
- the public configuration is documented in `configs/training-config.example.yml` and `configs/ai-toolkit-flux2dev-lora.example.yml`.

## Problem-To-Fix Mapping

| Problem | Practical Fix |
|---|---|
| CUDA OOM during training | custom training config, memory balancing, lower memory pressure |
| Workflow crashes | offloading and node-level adjustment |
| Slow iteration | more stable config and repeatable test loop |
| Weak LoRA consistency | dataset cleanup and trigger-word tuning |
| Overfitting/artifacts | adjust dataset and test early generations |

## Results Of Optimization

After tuning, the pipeline became more stable for:

- local FLUX2DEV inference;
- testing different prompts;
- using LoRA inside the inference workflow;
- running LoRA training experiments;
- comparing base model vs trained LoRA results.

## Technical Evidence

Training log capture:

![Training logs](../screenshots/training-logs.png)

The final results and before/after comparison are shown in [07-results.md](07-results.md).
