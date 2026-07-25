import unittest

from scripts.build_loss_chart import render_loss_chart


class LossChartTests(unittest.TestCase):
    def test_svg_is_rendered_without_embedding_raw_log_data(self) -> None:
        svg = render_loss_chart(
            [(0, 0.5), (1, 0.4), (2, 0.3)], title="Public run <001>"
        )
        self.assertIn("<svg", svg)
        self.assertIn("<polyline", svg)
        self.assertIn("Public run &lt;001&gt;", svg)
        self.assertNotIn("C:\\", svg)


if __name__ == "__main__":
    unittest.main()
