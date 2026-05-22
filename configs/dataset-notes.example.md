# Dataset Notes

This file describes the dataset structure used for the public FLUX2DEV LoRA training showcase.

## Dataset Summary

| Item | Value |
|---|---|
| Dataset size | 20-35 images |
| Source type | project-specific curated images |
| Cleaning tool | Photoshop |
| Captions | `.txt` sidecar files next to images |
| Trigger word | project-specific trigger word; public examples use `example_trigger` |
| Validation images | manual visual validation through sample generations |

## Preparation Steps

1. Collected source images.
2. Removed low-quality or duplicated images.
3. Cleaned selected images in Photoshop.
4. Prepared captions or trigger words.
5. Tested early LoRA output.
6. Adjusted dataset based on artifacts and consistency.

## Public Dataset Scope

The public dataset examples are limited to material that can be shared as part of the showcase. Private source material, copyrighted references, hidden metadata and local machine paths are outside the scope of this repository.
