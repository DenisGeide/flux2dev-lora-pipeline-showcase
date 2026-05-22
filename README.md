# FLUX2DEV LoRA Pipeline Showcase

Local FLUX2DEV inference and LoRA training showcase focused on ComfyUI workflow adaptation, memory optimization, dataset preparation and reproducible local generative AI experimentation.

> Engineering case study: running and tuning a heavy FLUX2DEV workflow locally, with a focus on VRAM pressure, OOM mitigation, LoRA training stability and before/after result comparison.

> This repository is a public technical showcase/tutorial. It documents the engineering process, not a full model release.  
> Model weights, LoRA weights, paid model files, private paths, secrets and unsafe training assets are not included.

## What Is This

This project documents how I ran FLUX2DEV locally through ComfyUI and trained LoRA experiments for FLUX2DEV with AI-Toolkit.

The goal was not just to generate images. The goal was to build a local workflow that is understandable, repeatable and stable enough for heavier inference and LoRA training experiments without relying on cloud GPU servers.

The repository has two main parts:

1. **FLUX2DEV inference pipeline**  
   ComfyUI setup, model placement, text encoder/VAE setup, workflow structure, sampler/guidance behavior and local memory constraints.

2. **FLUX2DEV LoRA training pipeline**  
   AI-Toolkit setup, dataset preparation, training configuration, OOM/crash mitigation, testing workflow and before/after result comparison.

## Why FLUX2DEV Is Hard Locally

FLUX2DEV is a heavy local workload. Running it is not just a "download model and click generate" task when the goal is stable high-load generation and LoRA training.

The main pain points:

- high VRAM pressure;
- OOM crashes during heavier experiments;
- memory fragmentation during longer sessions;
- unstable training configs;
- expensive iteration time when runs crash;
- sensitivity to sampler/guidance/noise settings;
- dataset quality strongly affecting LoRA results.

This showcase focuses on the engineering work around those problems: workflow adaptation, memory routing, training config tuning and repeatable evaluation.

## What This Project Demonstrates

- Local FLUX2DEV setup through ComfyUI.
- Adapted node-based inference workflow.
- Practical VRAM/RAM balancing for heavy local generation.
- OOM/crash debugging and stabilization.
- AI-Toolkit LoRA training workflow.
- Dataset preparation for LoRA training.
- Before/after comparison between base FLUX2DEV and trained LoRA.
- Documentation of a local GenAI workflow in a way another engineer can follow.

## Key Metrics

These values describe one working local experiment configuration, not a universal recipe.

Exact low-level settings changed during experiments depending on memory pressure, dataset behavior and output quality. This repository focuses on the final workflow structure, memory strategy and reproducible setup notes rather than presenting one fixed "perfect" config.

| Metric | Value |
|---|---|
| Base model | `flux2_dev.safetensors` |
| VAE | `flux2_vae.safetensors` |
| Runtime | ComfyUI |
| Launch method | `run_nvidia_gpu.bat` |
| Training framework | AI-Toolkit |
| CPU | AMD Ryzen 9 9950X3D |
| RAM | 128 GB |
| VRAM | 33 GB |
| OS | Windows 11 LTSC 24H2 |
| Dataset size | 20-35 images |
| Captions | `.txt` sidecar files |
| Training time | around 6-7 hours |
| Text encoder | `mistral_3.1_small_flux2_fp8.safetensors` |
| Training resolution | 768 |
| Training steps | 1800 |
| LoRA rank/alpha | 16 / 16 |
| Optimizer | `adamw8bit` |
| Learning rate | `0.0001` |
| Batch size | 1 |
| Gradient accumulation | 1 |
| Gradient checkpointing | enabled |
| Training dtype | `bf16` |
| Training noise scheduler | `flowmatch` |
| Sample size | 768x768 |
| Sample steps | 20 |
| Sample guidance | 1 |
| Training speed | varied by configuration and was monitored locally |

## Engineering Challenges

| Challenge | What Happened | How It Was Addressed |
|---|---|---|
| CUDA/OOM crashes | Heavy FLUX2DEV runs exceeded stable local memory limits | custom config tuning, offloading and memory balancing |
| VRAM pressure | The workflow pushed GPU memory hard during inference/training | node-level workflow adjustments and VRAM/RAM balancing |
| Training instability | Default-style configs were not stable enough for longer LoRA experiments | custom AI-Toolkit config and repeated test runs |
| Slow iteration | Failed runs made experimentation expensive in time | more stable baseline config and smaller validation loop |
| Output artifacts | Some settings produced weaker details or unstable outputs | sampler/guidance/noise tuning and dataset cleanup |
| Dataset sensitivity | Small LoRA datasets can overfit or introduce artifacts quickly | manual filtering, Photoshop cleanup and trigger-word control |

Full notes: [docs/04-optimization-notes.md](docs/04-optimization-notes.md)

## Hardware Setup

The pipeline was tested on a local GPU workstation.

| Component | Value |
|---|---|
| CPU | AMD Ryzen 9 9950X3D |
| RAM | 128 GB |
| VRAM | 33 GB |
| OS | Windows 11 LTSC 24H2 |
| Runtime | ComfyUI |
| Training framework | AI-Toolkit |

![Hardware overview](screenshots/hardware-overview-sanitized.png)

Details: [docs/01-environment-and-hardware.md](docs/01-environment-and-hardware.md)

## FLUX2DEV Inference Pipeline

The inference workflow was based on a community FLUX2DEV workflow and then manually adapted for my local setup.

Main areas of work:

- model loading;
- text encoder setup;
- VAE configuration;
- sampler chain tuning;
- guidance configuration;
- sigma/noise behavior;
- memory routing;
- high-resolution generation stability;
- LoRA-ready testing path.

![ComfyUI workflow overview](screenshots/comfyui-workflow-overview.png)

Annotated workflow:

![ComfyUI workflow annotated](screenshots/comfyui-workflow-annotated.png)

The annotated view highlights:

- model loading;
- text encoder block;
- guidance/CFG;
- sampler chain;
- sigma/noise logic;
- VAE decode;
- LoRA injection/testing path;
- memory-sensitive nodes.

Detailed pipeline breakdown: [docs/03-inference-pipeline.md](docs/03-inference-pipeline.md)

## LoRA Training Pipeline

LoRA training was performed with AI-Toolkit using FLUX2DEV as the base model.

The main work was not only the training itself, but stabilizing the training pipeline under high memory pressure.

Training notes:

- training framework: AI-Toolkit;
- dataset size: approximately 20-35 images;
- training time: around 6-7 hours;
- main issue: memory pressure / OOM;
- main fix: custom training config and memory balancing;
- LoRA weights are not published.

The published config is treated as a working reference, not a universal preset. FLUX2DEV training settings usually need to be adjusted for the GPU, dataset, target style and stability of each run.

Training config screenshot:

![Training config](screenshots/training-config.png)

Training log capture:

![Training logs](screenshots/training-logs.png)

Full training workflow: [docs/05-lora-training.md](docs/05-lora-training.md)

## Dataset Preparation

The dataset was prepared manually before training.

Dataset preparation included:

- selecting source images;
- removing low-quality images;
- cleaning/editing images in Photoshop;
- keeping the dataset consistent;
- preparing trigger words per LoRA target;
- testing early generations and adjusting the dataset if needed.

Dataset size:

```text
20-35 images
```

Dataset preview:

![Dataset preview](screenshots/dataset-preview.png)

Caption/trigger example:

![Caption example](screenshots/caption-example.png)

Dataset guide: [docs/06-dataset-preparation.md](docs/06-dataset-preparation.md)

## Results: Base vs LoRA

This is the most important visual section of the project. It shows why the engineering work mattered.

Visual summary:

| Base vs LoRA Comparison | Final Result Grid |
|---|---|
| <img src="screenshots/before-after-base-vs-lora.jpg" width="420"> | <img src="screenshots/final-results-grid.jpg" width="420"> |

Result notes focus on:

- prompt alignment;
- consistency;
- detail retention;
- texture quality;
- artifact reduction;
- stability under repeated local testing.

More results: [docs/07-results.md](docs/07-results.md)

## Config Examples

This repository includes public example configuration files. They are intentionally sanitized and omit private local paths and model assets.

| File | Purpose |
|---|---|
| [configs/comfyui-workflow.example.json](configs/comfyui-workflow.example.json) | sanitized workflow descriptor for the public pipeline structure |
| [configs/training-config.example.yml](configs/training-config.example.yml) | public training config template |
| [configs/ai-toolkit-flux2dev-lora.example.yml](configs/ai-toolkit-flux2dev-lora.example.yml) | sanitized AI-Toolkit config based on one working local experiment |
| [configs/dataset-notes.example.md](configs/dataset-notes.example.md) | dataset documentation template |

## How To Read This Repository

If you are new to FLUX2DEV/ComfyUI:

1. Start with [docs/01-environment-and-hardware.md](docs/01-environment-and-hardware.md).
2. Continue with [docs/02-flux2dev-comfyui-setup.md](docs/02-flux2dev-comfyui-setup.md).
3. Read [docs/03-inference-pipeline.md](docs/03-inference-pipeline.md) to understand the workflow.
4. Read [docs/05-lora-training.md](docs/05-lora-training.md) and [docs/06-dataset-preparation.md](docs/06-dataset-preparation.md) for the training side.
5. Finish with [docs/07-results.md](docs/07-results.md).

If you are reviewing this as a technical showcase, the most important sections are:

- [docs/03-inference-pipeline.md](docs/03-inference-pipeline.md)
- [docs/04-optimization-notes.md](docs/04-optimization-notes.md)
- [docs/05-lora-training.md](docs/05-lora-training.md)
- [docs/07-results.md](docs/07-results.md)

## Repository Structure

```text
flux2dev-lora-pipeline-showcase/
|-- README.md
|-- docs/
|   |-- 01-environment-and-hardware.md
|   |-- 02-flux2dev-comfyui-setup.md
|   |-- 03-inference-pipeline.md
|   |-- 04-optimization-notes.md
|   |-- 05-lora-training.md
|   |-- 06-dataset-preparation.md
|   +-- 07-results.md
|-- configs/
|   |-- comfyui-workflow.example.json
|   |-- ai-toolkit-flux2dev-lora.example.yml
|   |-- training-config.example.yml
|   +-- dataset-notes.example.md
|-- screenshots/
|   |-- comfyui-workflow-overview.png
|   |-- comfyui-workflow-annotated.png
|   |-- hardware-overview-sanitized.png
|   |-- model-files.png
|   |-- training-config.png
|   |-- training-logs.png
|   |-- dataset-preview.png
|   |-- caption-example.png
|   |-- before-after-base-vs-lora.jpg
|   +-- final-results-grid.jpg
|-- results/
|   +-- README.md
|-- LICENSE
+-- .gitignore
```

## External References

- [FLUX.2 by Black Forest Labs](https://bfl.ai/models/flux2)
- [ComfyUI GitHub](https://github.com/comfy-org/ComfyUI)
- [ComfyUI official documentation](https://docs.comfy.org/)
- [AI-Toolkit by Ostris](https://github.com/ostris/ai-toolkit)

## Not Included

This repository does not include:

- private model weights;
- paid model files;
- LoRA weights;
- unsafe or non-public training assets;
- private local paths;
- machine-specific secrets;
- API keys or tokens.

## Public Note

This is a public showcase/tutorial repository. Some implementation details are simplified or sanitized to avoid publishing private files, paid model assets, copyrighted material or machine-specific configuration.

The focus is on explaining the engineering process: setup, optimization, dataset preparation, training workflow and results.

## License

Documentation and example configuration files in this repository are released under the [MIT License](LICENSE).

Model files, LoRA weights, private datasets, paid model assets and third-party assets are not included in this repository and are not covered by this license.
