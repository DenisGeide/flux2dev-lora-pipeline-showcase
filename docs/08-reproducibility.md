# Reproducibility guide

This repository does not vendor a trainer or model weights. It provides
sanitized AI-Toolkit configs, a dataset manifest contract, log parsing, an
experiment registry, and the original project screenshots and result previews.
You supply licensed data and obtain model access from the model publisher.

## 1. Record the environment

The historical audit used
[`ostris/ai-toolkit`](https://github.com/ostris/ai-toolkit) at observed revision:

```text
35b1cde3cb7b0151a51bf8547bab0931fd57d72d
```

That revision is provenance, not a promise that it remains the best version.
Record your own environment before training:

```bash
python --version
nvidia-smi
git -C /path/to/ai-toolkit rev-parse HEAD
python -m pip freeze > environment.lock.txt
```

Do not commit tokens or a private package cache. Store `environment.lock.txt`
with the run artifacts if it contains no private registry URLs.

## 2. Prepare licensed data

Use [`data/dataset-manifest.schema.json`](../data/dataset-manifest.schema.json)
and validate the manifest:

```bash
python scripts/validate_dataset_manifest.py path/to/manifest.json \
  --dataset-root path/to/dataset
```

The expected training layout remains image files with matching UTF-8 `.txt`
sidecars. The public manifest records provenance, rights, split, dimensions,
and optional hashes without embedding image content.

## 3. Choose a config

- FLUX.1 reference: [`configs/ai-toolkit-flux1dev-lora.example.yml`](../configs/ai-toolkit-flux1dev-lora.example.yml)
- FLUX.2 reference: [`configs/ai-toolkit-flux2dev-lora.example.yml`](../configs/ai-toolkit-flux2dev-lora.example.yml)

Replace only documented placeholders first. Keep a copy of the final config
next to each run. The FLUX.1 reference is shaped from the completed historical
run, with sanitized prompts and a fixed validation seed. The FLUX.2 reference
is informed by historical attempts but is not backed by an unambiguous complete
log in the audited workspace.

## 4. Smoke-test before a long run

Start with:

- 10–20 steps;
- one validation prompt;
- the intended resolution;
- the intended quantization/offloading strategy.

Confirm that model loading, latent caching, the first optimizer step, sampling,
and checkpoint writing all succeed. A smoke test catches the pre-training OOM
failures documented in this project without wasting a full run.

## 5. Run AI-Toolkit

From an AI-Toolkit checkout, the upstream CLI pattern is:

```bash
python run.py path/to/config.yml
```

Follow upstream installation and model-access instructions. This repository
does not redistribute the model or override its terms.

## 6. Extract a safe report

Keep the raw log private, then produce path-free summaries:

```bash
python scripts/parse_training_log.py path/to/log.txt \
  --run-id public-run-001 \
  --output reports/public-run-001.json \
  --markdown-output reports/public-run-001.md \
  --series-output reports/public-run-001.csv

python scripts/build_loss_chart.py reports/public-run-001.csv \
  --output reports/public-run-001-loss.svg \
  --title "public-run-001 training loss"
```

The parser emits progress, loss summaries, speed, checkpoint counts, OOM status,
and an optional deduplicated metric series. The chart script turns that series
into a standalone SVG without plotting dependencies. Neither tool copies raw
lines, paths, prompts, trigger words, or filenames.

## 7. Run a real controlled comparison

The historical records are observational because datasets and several settings
changed together. For a controlled study:

1. freeze the dataset manifest and train/validation split;
2. freeze the base model, software revision, seed, resolution, optimizer, and prompts;
3. vary one parameter only;
4. use identical validation seeds;
5. record wall time, speed, peak VRAM, loss, and checkpoint size;
6. review a fixed output grid blind to run ID;
7. report failed runs as results, not as missing data.

Use [`configs/controlled-study.example.yml`](../configs/controlled-study.example.yml)
as the protocol record. Do not call the comparison an ablation until these
conditions are met.

## Reproduction boundary

Exact pixel reproduction can still vary with GPU kernels, library versions, and
non-deterministic operations. The target here is auditable process
reproducibility: known inputs, versioned configuration, fixed evaluation, and
honest reporting of variance and failures.
