# Results

This page shows the visible outcome of the FLUX2DEV LoRA experiments and connects the final images with the engineering work described in the earlier documents.

The goal of the result section is simple: show the difference between the base FLUX2DEV output and the trained LoRA output, then show several final generations produced through the stabilized local workflow.

## Base FLUX2DEV vs Trained LoRA

![Base FLUX2DEV vs trained LoRA](../screenshots/before-after-base-vs-lora.jpg)

This comparison demonstrates the practical purpose of the pipeline: the base model is used as the starting point, while the trained LoRA is evaluated for consistency, prompt alignment, detail retention and artifact reduction.

## Final Result Grid

![Final result grid](../screenshots/final-results-grid.jpg)

The result grid is used as a quick visual summary of the final local workflow. It shows multiple generations from the same optimized setup instead of relying on a single best image.

## Evaluation Focus

The results are evaluated through engineering-oriented criteria:

- prompt alignment;
- detail retention;
- texture quality;
- visual consistency;
- artifact reduction;
- stable behavior across repeated local tests.

## Result Context

The exact generation settings changed during experiments. The repository therefore treats results as outputs of a tuned local pipeline, not as proof that one fixed sampler/configuration is universally optimal.

The important part is the repeatable workflow:

1. prepare and clean the dataset;
2. train LoRA through AI-Toolkit;
3. test LoRA inside the ComfyUI workflow;
4. compare base output against LoRA output;
5. keep the configuration stable enough for repeated local evaluation.
