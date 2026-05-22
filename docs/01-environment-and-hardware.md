# Environment And Hardware

This document describes the local environment used for FLUX2DEV inference and LoRA training.

The purpose of this page is to help readers understand the hardware constraints behind the project. FLUX2DEV and LoRA training are heavy workloads, so the environment matters as much as the model configuration.

## Hardware Summary

| Component | Value |
|---|---|
| CPU | AMD Ryzen 9 9950X3D |
| RAM | 128 GB |
| VRAM | 33 GB |
| OS | Windows 11 LTSC 24H2 |
| Runtime | ComfyUI |
| Training framework | AI-Toolkit |

![Hardware overview](../screenshots/hardware-overview-sanitized.png)

The screenshot is sanitized and used only to show the hardware class used for the local experiments.

## Software Environment

| Component | Value |
|---|---|
| Runtime | [ComfyUI](https://github.com/comfy-org/ComfyUI) |
| Documentation | [ComfyUI docs](https://docs.comfy.org/) |
| Launch method | `run_nvidia_gpu.bat` |
| Base model | `flux2_dev.safetensors` |
| VAE | `flux2_vae.safetensors` |
| LoRA training | [AI-Toolkit](https://github.com/ostris/ai-toolkit) |

Exact Python/CUDA/PyTorch/ComfyUI/AI-Toolkit versions can change over time, so this showcase documents the hardware class, workflow structure and config strategy instead of locking the project to one machine-specific dependency snapshot.

For a production reproduction attempt, record the local versions before running experiments:

```text
python --version
nvidia-smi
pip freeze
git rev-parse HEAD
```

## Why This Setup Needed Optimization

FLUX2DEV is a heavy local workload. A simple "load model and press generate" setup can become unstable when the workflow uses high resolution, large text encoders, LoRA nodes, sampler chains and long running sessions.

The main engineering constraints were:

- high VRAM pressure;
- OOM errors during heavier experiments;
- memory fragmentation during longer sessions;
- slower iteration when runs crashed;
- need to balance GPU VRAM and system RAM.

## What The Hardware Enabled

The local workstation made it possible to:

- run FLUX2DEV locally without depending on cloud GPU servers;
- iterate on ComfyUI workflow changes;
- test LoRA outputs inside the same inference pipeline;
- train LoRA experiments locally;
- debug memory-related failures directly.

## Notes For Readers With Different Hardware

This setup is not a minimum requirement. It documents the environment used for this showcase.

If you have less VRAM, you may need to:

- reduce resolution;
- reduce batch size;
- simplify the workflow;
- use stronger offloading;
- use quantized/optimized variants where appropriate;
- test smaller settings before running high-load generations.
