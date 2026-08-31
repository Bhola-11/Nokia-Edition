import unittest
from apps.game.bosses.boss_01_colossus import BossEncounter_colossus
from apps.game.bosses.boss_15_ouroboros_prime import BossEncounter_ouroboros_prime
from apps.game.powerups.powerup_speed_surge import Powerup_speed_surge
from apps.game.powerups.powerup_shield_aura import Powerup_shield_aura

class BossAndPowerupTestCase(unittest.TestCase):
    def test_boss_damage_and_phase(self):
        boss = BossEncounter_colossus()
        self.assertEqual(boss.phase, 1)
        res = boss.take_damage(350)
        self.assertEqual(res["phase"], 2)
        self.assertFalse(res["is_defeated"])

    def test_final_boss_rage_mode(self):
        boss = BossEncounter_ouroboros_prime()
        res = boss.take_damage(int(boss.max_hp * 0.8))
        self.assertEqual(boss.phase, 3)
        self.assertTrue(boss.rage_mode)

    def test_powerup_lifecycle(self):
        p = Powerup_speed_surge(duration_sec=5.0)
        p.activate()
        self.assertTrue(p.is_active)
        expired = p.tick_decay(6.0)
        self.assertTrue(expired)
        self.assertFalse(p.is_active)

    def test_shield_powerup(self):
        shield = Powerup_shield_aura(duration_sec=10.0)
        shield.activate()
        self.assertEqual(shield.remaining_sec, 10.0)
