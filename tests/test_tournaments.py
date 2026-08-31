import unittest
from apps.tournaments.matchmaking.elo_glicko import EloGlickoRatingEngine
from apps.tournaments.matchmaking.swiss_engine import SwissTournamentEngine

class TournamentEngineTestCase(unittest.TestCase):
    def test_elo_calculation(self):
        engine = EloGlickoRatingEngine(base_rating=1200)
        new_r1, new_r2 = engine.update_ratings("player1", "player2")
        self.assertGreater(new_r1, 1200)
        self.assertLess(new_r2, 1200)
