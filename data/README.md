# Dataset manifests

The historical source photographs and captions are **not** stored in this
repository. This folder provides a portable manifest format so another user can
prepare a compatible, licensed dataset without inheriting private paths or data.

## Expected layout

```text
my-dataset/
|-- manifest.json
|-- images/
|   |-- subject-001.webp
|   +-- subject-002.webp
+-- captions/
    |-- subject-001.txt
    +-- subject-002.txt
```

Each image must have a UTF-8 `.txt` sidecar. Keep trigger tokens synthetic and
stable; do not use a person's real name unless you have a lawful reason and
explicit permission.

## Validate

Validate metadata only:

```bash
python scripts/validate_dataset_manifest.py data/dataset-manifest.example.json
```

Validate a real manifest, referenced files, and optional SHA-256 digests:

```bash
python scripts/validate_dataset_manifest.py path/to/manifest.json \
  --dataset-root path/to/my-dataset
```

The validator rejects absolute paths, `..` traversal, and unknown nested
fields so generated public metadata cannot accidentally expose a local
workstation path. It also requires
`rights.public_release_approved: true` and
`rights.contains_personal_data: false`; a manifest that fails either release
gate is intentionally rejected.

## Local audit context

The private historical workspace contained four curated datasets with 98 images
and 98 caption files in total (34, 16, 32, and 16 images). A stem-level audit
found 97 correct pairs plus one unmatched image and one unmatched caption in
the 32-image dataset. These aggregate counts are included for provenance and
data-quality transparency only. They are not a redistribution license.

Before publishing any dataset, confirm all of the following:

- you own the images or have redistribution rights;
- depicted people consent to the intended use;
- captions contain no personal or secret information;
- EXIF and other hidden metadata have been removed;
- the manifest contains a clear dataset license;
- the split and hashes match the released files.
