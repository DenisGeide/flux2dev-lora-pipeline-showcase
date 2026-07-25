from pathlib import Path
import unittest

from scripts.parse_training_log import extract_training_series, parse_training_log


FIXTURES = Path(__file__).parent / "fixtures"


class ParseTrainingLogTests(unittest.TestCase):
    def test_completed_log_is_deduplicated_and_sanitized(self) -> None:
        summary = parse_training_log(
            (FIXTURES / "completed.log").read_text(encoding="utf-8"),
            run_id="fixture-complete",
        )

        self.assertEqual(summary["status"], "completed")
        self.assertEqual(summary["progress"]["unique_reported_steps"], 3)
        self.assertEqual(summary["progress"]["max_reported_step"], 2)
        self.assertEqual(summary["progress"]["progress_percent"], 100.0)
        self.assertEqual(summary["optimization"]["last_reported_loss"], 0.3)
        self.assertEqual(summary["events"]["final_checkpoint_events"], 1)
        self.assertFalse(summary["privacy"]["paths_included"])
        self.assertNotIn("private", str(summary))
        series = extract_training_series(
            (FIXTURES / "completed.log").read_text(encoding="utf-8")
        )
        self.assertEqual(len(series), 3)
        self.assertEqual(series[-1]["loss"], 0.3)

    def test_oom_before_training_is_reported(self) -> None:
        summary = parse_training_log(
            (FIXTURES / "oom.log").read_text(encoding="utf-8"),
            run_id="fixture-oom",
        )

        self.assertEqual(summary["status"], "failed_oom")
        self.assertIsNone(summary["progress"]["max_reported_step"])
        self.assertTrue(summary["events"]["cuda_oom_detected"])

    def test_final_checkpoint_without_terminal_progress_is_not_completed(self) -> None:
        early_log = "\n".join(
            [
                "3/100 [00:01<00:33, 0.33s/it, lr: 1e-4 loss: 0.8]",
                "Saved checkpoint to C:/private/run/adapter.safetensors",
            ]
        )
        summary = parse_training_log(early_log, run_id="fixture-mixed")

        self.assertEqual(summary["status"], "mixed_evidence")
        self.assertEqual(summary["progress"]["max_reported_step"], 3)
        self.assertEqual(summary["progress"]["target_steps"], 100)
        self.assertEqual(summary["events"]["final_checkpoint_events"], 1)
        self.assertFalse(summary["privacy"]["paths_included"])
        self.assertNotIn("private", str(summary))

    def test_final_checkpoint_without_progress_is_not_completed(self) -> None:
        summary = parse_training_log(
            "Saved checkpoint to C:/private/run/adapter.safetensors",
            run_id="fixture-no-progress",
        )

        self.assertEqual(summary["status"], "mixed_evidence")
        self.assertIsNone(summary["progress"]["target_steps"])
        self.assertIsNone(summary["progress"]["max_reported_step"])


if __name__ == "__main__":
    unittest.main()
