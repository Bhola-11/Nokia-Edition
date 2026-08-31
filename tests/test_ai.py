import unittest
from apps.game.ai.astar_pathfinder import AStarPathfinderBot
from apps.game.ai.hamiltonian_cycle import HamiltonianCycleBot
from apps.game.ai.floodfill_survival import FloodFillSurvivalBot

class AIBotsTestCase(unittest.TestCase):
    def test_astar_decision(self):
        bot = AStarPathfinderBot()
        snake = [(10, 8), (9, 8), (8, 8)]
        food = (15, 8)
        move = bot.evaluate_next_move(snake, food, set())
        self.assertIn(move, ["U", "D", "L", "R"])
        self.assertEqual(move, "R")

    def test_floodfill_survival(self):
        bot = FloodFillSurvivalBot()
        snake = [(5, 5), (5, 6), (5, 7)]
        food = (5, 1)
        move = bot.evaluate_next_move(snake, food, set())
        self.assertIn(move, ["U", "D", "L", "R"])
