# Failure modes and recovery

Historical failures are first-class evidence in this project. Three available
logs end in CUDA OOM before a training step, and several run folders retain only
numbered checkpoints. The table below turns those observations into a practical
debugging order.

| Symptom | Observed stage | Likely pressure point | First checks |
|---|---|---|---|
| OOM while quantizing transformer blocks | model load | quantization temporarily needs more memory than expected | close other GPU processes, restart the process, verify quantization/offloading compatibility |
| OOM after model and VAE load | model preparation | model plus preparation buffers exceed available VRAM | enable low-VRAM/offloading strategy, reduce competing GPU use, smoke-test the exact config |
| Numbered checkpoints but no final adapter | mid-run or external stop | interruption, manual stop, process failure, or storage issue | inspect the private log, verify free disk, resume only from a documented compatible state |
| Final artifact plus a later OOM log in one folder | reused run name/folder | evidence from multiple attempts was mixed | use immutable run IDs and a new output directory for every attempt |
| Weak subject consistency | evaluation | insufficient or inconsistent coverage | audit captions, duplicates, framing, and trigger-token use |
| Background/style leakage | evaluation | dataset correlation | diversify backgrounds and hold out validation compositions |
| Increasing artifacts at later checkpoints | evaluation | overfitting or aggressive learning rate | compare fixed-seed checkpoints and stop earlier |

## Safe triage order

1. Preserve the raw log and config privately.
2. Assign a unique run ID; never reuse the old output directory.
3. Identify whether failure occurred during model load, caching, training, sampling, or saving.
4. Reproduce with a 10–20-step smoke run.
5. Change one memory control at a time.
6. Re-run the same validation prompts and seeds.
7. Record the failed attempt in the registry.

## What not to infer

- A checkpoint file alone does not prove a run reached the configured target.
- An unnumbered adapter and an unrelated retry log must not be combined into one claim.
- Lower training loss alone does not prove better visual quality.
- Runs on different datasets are not hyperparameter ablations.
- Quantization, low-VRAM mode, and offloading are not interchangeable switches;
  compatibility depends on model architecture and AI-Toolkit revision.

The public registry applies these rules conservatively. See
[`experiments/README.md`](../experiments/README.md).
