from collections import defaultdict
import unittest

import pandas as pd

from src.build_marts import METRICS, _blank_metrics, _to_frame


class MartLogicTests(unittest.TestCase):
    def test_rate_calculation_uses_valid_timeliness_denominator(self):
        accumulator = defaultdict(_blank_metrics)
        accumulator[("Example",)] = [100, 97, 3, 2, 10, 70]
        result = _to_frame(accumulator, ["product"]).iloc[0]
        self.assertEqual(result["timely_rate"], 0.97)
        self.assertEqual(result["monetary_relief_rate"], 0.02)
        self.assertEqual(result["public_response_rate"], 0.70)


    def test_blank_metrics_matches_metric_contract(self):
        self.assertEqual(len(_blank_metrics()), len(METRICS))
        self.assertTrue(all(value == 0 for value in _blank_metrics()))


if __name__ == "__main__":
    unittest.main()
