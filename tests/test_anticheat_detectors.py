import unittest
from apps.anticheat.detectors.jitter_analyzer import InputJitterAnalyzer
from apps.anticheat.detectors.signature_checker import CryptographicSignatureChecker

class AntiCheatDetectorsTestCase(unittest.TestCase):
    def test_bot_jitter_detection(self):
        analyzer = InputJitterAnalyzer()
        bot_intervals = [20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0]
        report = analyzer.analyze_event_sequence(bot_intervals)
        self.assertTrue(report["is_suspicious"])

    def test_human_jitter_normal(self):
        analyzer = InputJitterAnalyzer()
        human_intervals = [120.0, 85.0, 140.0, 95.0, 110.0, 130.0]
        report = analyzer.analyze_event_sequence(human_intervals)
        self.assertFalse(report["is_suspicious"])
