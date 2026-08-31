import unittest
from apps.game.levels.level_01 import get_level_01_instance
from apps.game.levels.level_10 import get_level_10_instance
from apps.game.levels.level_25 import get_level_25_instance
from apps.game.levels.level_50 import get_level_50_instance

class LevelSystemTestCase(unittest.TestCase):
    def test_level_01_initialization(self):
        engine = get_level_01_instance()
        self.assertEqual(engine.config.level_id, "level_01")
        self.assertEqual(engine.config.grid_width, 28)
        self.assertEqual(engine.config.grid_height, 16)
        self.assertIsInstance(engine.config.wall_coordinates, list)

    def test_level_10_portals(self):
        engine = get_level_10_instance()
        self.assertTrue(engine.config.teleport_enabled)
        teleport_exit = engine.resolve_portal_passage(2, 2)
        self.assertIsNotNone(teleport_exit)

    def test_level_score_weighting(self):
        engine = get_level_25_instance()
        score = engine.calculate_score_weight(raw_apples=10, survival_time_sec=45.0)
        self.assertGreater(score, 100)

    def test_level_50_spawn_coordinates(self):
        engine = get_level_50_instance()
        spawn = engine.generate_valid_spawn_coordinates(occupied_set={(0, 0), (1, 1)})
        self.assertIsNotNone(spawn)
        self.assertNotIn(spawn, engine.config.wall_coordinates)
