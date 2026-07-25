# Attribution and license boundaries

This repository is an experiment, documentation, and evaluation layer. The
training implementation is **not** authored here.

## Third-party components

### AI-Toolkit

- Project: [`ostris/ai-toolkit`](https://github.com/ostris/ai-toolkit)
- Role: LoRA trainer and training runtime
- License observed in the local checkout: MIT
- Locally audited revision: `35b1cde3cb7b0151a51bf8547bab0931fd57d72d`

The sanitized YAML files follow AI-Toolkit's configuration shape. Review the
upstream project and license before use because its API and dependencies can
change.

### ComfyUI

- Project: [`comfy-org/ComfyUI`](https://github.com/comfy-org/ComfyUI)
- Role: node-based inference and adapter evaluation runtime

### FLUX models

- Publisher: [Black Forest Labs](https://bfl.ai/)
- Role: third-party base models

Model files are not included. Obtain them from an authorized source and comply
with the terms attached to the exact model/version you use.

## Original work in this repository

- sanitized experiment configurations;
- historical evidence audit and conservative status classification;
- path-free log parser;
- generated experiment report;
- dataset manifest schema and validator;
- reproducibility and failure-analysis documentation;
- adapted ComfyUI workflow documentation;
- original sanitized SVG diagrams that explain the workflow and evaluation
  protocol without reproducing private outputs.

## Repository license

The original code, documentation, and examples in this repository are released
under [`LICENSE`](../LICENSE). That license does not relicense third-party
models, training data, AI-Toolkit, ComfyUI, the retained third-party file-name
screenshot, or privately held LoRA adapters and generated images.
