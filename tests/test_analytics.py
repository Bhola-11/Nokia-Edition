import unittest
from apps.analytics.telemetry.heatmap_generator import MovementHeatmapGenerator
from apps.analytics.telemetry.survival_curve import KaplanMeierSurvivalCurveEstimator

class AnalyticsTelemetryTestCase(unittest.TestCase):
    def test_heatmap_density_matrix(self):
        gen = MovementHeatmapGenerator()
        coords = [(5, 5), (5, 5), (5, 5), (6, 5), (7, 5)]
        heatmap = gen.build_density_map(coords, 28, 16)
        self.assertEqual(len(heatmap), 16)
        self.assertEqual(len(heatmap[0]), 28)
        self.assertEqual(heatmap[5][5], 1.0)
