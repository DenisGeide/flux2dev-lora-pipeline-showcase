# Data card

## Public release scope

No historical source photograph, private caption, cached latent, or EXIF record
is distributed by this repository. Public SVGs are repo-native explanatory
diagrams made from text and geometric shapes; they are not source photographs,
generated results, or a downloadable training corpus.

The repository publishes:

- aggregate historical counts;
- a JSON Schema for portable dataset manifests;
- a synthetic two-record manifest example;
- validation tooling;
- strict public-release and personal-data gates;
- preparation and rights-review guidance.

## Historical aggregate

The local audit found four curated datasets containing 98 images and 98 caption
files. Stem matching produced 97 correct pairs:

| Sanitized dataset | Images | Captions | Matched |
|---|---:|---:|---:|
| `private-dataset-a` | 32 | 32 | 31 |
| `private-dataset-b` | 34 | 34 | 34 |
| `private-dataset-c` | 16 | 16 | 16 |
| `private-dataset-d` | 16 | 16 | 16 |
| **Total** | **98** | **98** | **97** |

Dataset IDs are intentionally disconnected from private subject names. The
counts document experiment provenance and do not grant redistribution rights.
Dataset A contains one unmatched image and one unmatched caption filename.

## Format

- common image formats: PNG, JPEG, or WebP;
- one UTF-8 `.txt` sidecar per image;
- one stable trigger token per intended target when needed;
- explicit `train`, `validation`, or `test` split in the manifest;
- optional SHA-256 image digest.

## Preparation

1. remove duplicates, low-quality images, and accidental screenshots;
2. inspect subject and background diversity;
3. crop/clean only when the edit does not misrepresent rights or provenance;
4. write factual, consistent captions;
5. remove hidden metadata;
6. hold out validation compositions;
7. document ownership, consent, and license.

## Known risks

- Small subject datasets can overfit identity, clothing, or backgrounds.
- Caption conventions can leak the target into unrelated concepts.
- Personal photographs can contain biometric and location information.
- A user owning a file does not necessarily own redistribution or model-training rights.
- Generated validation images may still reveal characteristics of the training target.

Anyone publishing a compatible dataset is responsible for verifying ownership,
consent, local law, model terms, and the chosen dataset license.
