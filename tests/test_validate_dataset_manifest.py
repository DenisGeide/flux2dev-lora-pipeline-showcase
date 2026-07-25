from copy import deepcopy
import json
from pathlib import Path
import unittest

from scripts.validate_dataset_manifest import validate_manifest


ROOT = Path(__file__).resolve().parents[1]


class DatasetManifestTests(unittest.TestCase):
    def test_public_example_is_structurally_valid(self) -> None:
        manifest = json.loads(
            (ROOT / "data" / "dataset-manifest.example.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(validate_manifest(manifest), [])

    def test_absolute_and_traversal_paths_are_rejected(self) -> None:
        manifest = {
            "schema_version": "1.0",
            "dataset_id": "unsafe",
            "version": "1",
            "license": "CC0-1.0",
            "rights": {
                "basis": "test",
                "public_release_approved": True,
                "contains_personal_data": False,
            },
            "items": [
                {
                    "id": "bad",
                    "image": "C:/private/photo.png",
                    "caption": "../secret.txt",
                    "split": "train",
                }
            ],
        }
        errors = validate_manifest(manifest)
        self.assertEqual(len(errors), 2)
        self.assertTrue(all("safe relative path" in error for error in errors))

    def test_public_release_must_be_approved_and_personal_data_free(self) -> None:
        manifest = json.loads(
            (ROOT / "data" / "dataset-manifest.example.json").read_text(
                encoding="utf-8"
            )
        )
        manifest["rights"]["public_release_approved"] = False
        manifest["rights"]["contains_personal_data"] = True

        errors = validate_manifest(manifest)

        self.assertIn("rights.public_release_approved must be true", errors)
        self.assertIn("rights.contains_personal_data must be false", errors)

    def test_unknown_rights_and_item_fields_are_rejected(self) -> None:
        manifest = json.loads(
            (ROOT / "data" / "dataset-manifest.example.json").read_text(
                encoding="utf-8"
            )
        )
        manifest = deepcopy(manifest)
        manifest["rights"]["private_note"] = "must not leak"
        manifest["items"][0]["local_path"] = "D:/private/source.webp"

        errors = validate_manifest(manifest)

        self.assertIn("unexpected rights fields: private_note", errors)
        self.assertIn("items[0] has unexpected fields: local_path", errors)


if __name__ == "__main__":
    unittest.main()
