# Dataset Notes

This file is a short human-readable companion to the machine-readable dataset
manifest. Copy it into a licensed dataset release and replace every placeholder.

## Dataset Summary

| Item | Value |
|---|---|
| Dataset size | record the exact count |
| Source type | owned, licensed, or synthetic material |
| Cleaning tool | Photoshop |
| Captions | `.txt` sidecar files next to images |
| Trigger word | use a synthetic token; public examples use `synthetic_object_token` |
| Validation images | manual visual validation through sample generations |

## Preparation Steps

1. Collected source images.
2. Removed low-quality or duplicated images.
3. Cleaned selected images in Photoshop.
4. Prepared captions or trigger words.
5. Tested early LoRA output.
6. Adjusted dataset based on artifacts and consistency.

## Required public files

- a manifest following [`../data/dataset-manifest.schema.json`](../data/dataset-manifest.schema.json);
- image files;
- one UTF-8 `.txt` caption per image;
- a dataset license;
- a short data card covering rights, consent, limitations, and intended use.

## Public dataset scope

The historical audit found 98 images and 98 captions across four private
datasets, with 97 correctly matched stems and one mismatch. Those files are not
part of the public release. Publish only material for which redistribution and
training use are authorized, and run the manifest validator first.
