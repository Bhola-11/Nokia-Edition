from django.test import TestCase, Client
from django.contrib.auth.models import User
from apps.game.models import GameSession, Score, GameMap
from apps.anticheat.engine import AntiCheatEngine, DeterministicRNG
from apps.achievements.models import Achievement, PlayerAchievement
from apps.achievements.evaluator import AchievementEvaluator
import json

class AntiCheatEngineTestCase(TestCase):
    def test_deterministic_rng(self):
        rng1 = DeterministicRNG(42)
        rng2 = DeterministicRNG(42)
        vals1 = [rng1.nextInt(0, 100) for _ in range(10)]
        vals2 = [rng2.nextInt(0, 100) for _ in range(10)]
        self.assertEqual(vals1, vals2)

    def test_valid_gameplay_simulation(self):
        # Seed 42 simulation
        seed = 42
        moves = [
            {'t': 0, 'd': 'R', 'ms': 100},
            {'t': 5, 'd': 'D', 'ms': 600},
            {'t': 10, 'd': 'L', 'ms': 1100},
            {'t': 15, 'd': 'U', 'ms': 1600},
        ]
        report = AntiCheatEngine.validate_session(
            session_seed=seed,
            mode='classic',
            difficulty='normal',
            reported_score=0,
            apples_eaten=0,
            max_length=3,
            duration_sec=2.0,
            moves_data=moves
        )
        self.assertTrue(report['is_valid'])

    def test_flagged_impossible_score(self):
        # Claiming 500 points with 0 moves
        report = AntiCheatEngine.validate_session(
            session_seed=42,
            mode='classic',
            difficulty='normal',
            reported_score=500,
            apples_eaten=30,
            max_length=33,
            duration_sec=5.0,
            moves_data=[]
        )
        self.assertFalse(report['is_valid'])


class GameAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='password123')

    def test_start_session_api(self):
        response = self.client.post(
            '/api/session/start/',
            data=json.dumps({'mode': 'classic', 'difficulty': 'normal'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertTrue('session_id' in data)
        self.assertTrue('seed' in data)

    def test_submit_valid_score_api(self):
        # Start session
        res_start = self.client.post(
            '/api/session/start/',
            data=json.dumps({'mode': 'classic', 'difficulty': 'normal'}),
            content_type='application/json'
        )
        session_id = res_start.json()['session_id']

        self.client.login(username='tester', password='password123')
        res_submit = self.client.post(
            '/api/session/submit/',
            data=json.dumps({
                'session_id': session_id,
                'score': 0,
                'apples_eaten': 0,
                'max_length': 3,
                'duration_seconds': 1.5,
                'death_reason': 'wall',
                'moves_data': [{'t': 1, 'd': 'R', 'ms': 100}]
            }),
            content_type='application/json'
        )
        self.assertEqual(res_submit.status_code, 200)
        data = res_submit.json()
        self.assertEqual(data['status'], 'verified')
