import json
from pathlib import Path
import unittest

from scripts.build_experiment_report import render_registry


ROOT = Path(__file__).resolve().parents[1]


class ExperimentRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = json.loads(
            (ROOT / "experiments" / "registry.json").read_text(encoding="utf-8")
        )

    def test_audit_counts_match_run_records(self) -> None:
        audit = self.registry["source_audit"]
        runs = self.registry["runs"]
        self.assertEqual(len(runs), audit["configuration_files"])
        self.assertEqual(
            sum(run["observed"]["checkpoint_files"] for run in runs),
            audit["checkpoint_files"],
        )
        self.assertEqual(
            sum(run["observed"].get("validation_images", 0) for run in runs),
            audit["validation_images"],
        )
        self.assertEqual(audit["image_files"], 98)
        self.assertEqual(audit["caption_files"], 98)
        self.assertEqual(audit["matched_image_caption_pairs"], 97)
        self.assertEqual(audit["unmatched_image_files"], 1)
        self.assertEqual(audit["unmatched_caption_files"], 1)
        for run in runs:
            self.assertLessEqual(
                run["config"]["matched_caption_pairs"],
                run["config"]["dataset_images"],
            )

    def test_registry_is_sanitized(self) -> None:
        serialized = json.dumps(self.registry, ensure_ascii=False).lower()
        forbidden = (
            "c:\\",
            "c:/",
            "users/unknown",
            "ai-toolkit-easy-install-main",
        )
        for value in forbidden:
            self.assertNotIn(value, serialized)

    def test_public_visuals_are_repo_native_illustrations(self) -> None:
        visuals = self.registry["public_visuals"]
        self.assertFalse(visuals["model_outputs_included"])
        self.assertEqual(visuals["kind"], "sanitized_repo_native_illustrations")
        self.assertEqual(len(visuals["artifacts"]), 5)
        for relative in visuals["artifacts"]:
            self.assertTrue(relative.endswith("-illustrative.svg"))
            path = ROOT / relative
            self.assertTrue(path.is_file(), relative)
            content = path.read_text(encoding="utf-8")
            self.assertIn("SANITIZED ILLUSTRATION", content)
            self.assertNotIn("<image", content.lower())

    def test_checked_in_report_is_generated_from_registry(self) -> None:
        checked_in = (ROOT / "experiments" / "README.md").read_text(encoding="utf-8")
        self.assertEqual(checked_in, render_registry(self.registry))


if __name__ == "__main__":
    unittest.main()
