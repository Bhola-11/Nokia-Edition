import unittest
from apps.game.physics.toroidal_geometry import ToroidalGeometryEngine
from apps.game.physics.collision_subsystem import CollisionMatrixSubsystem

class PhysicsSubsystemsTestCase(unittest.TestCase):
    def test_toroidal_step(self):
        engine = ToroidalGeometryEngine()
        engine.entities.append({"x": 27.5, "y": 8.0, "velocity": (1.0, 0.0)})
        engine.step_simulation(0.1)
        self.assertGreater(engine.entities[0]["x"], 27.5)

    def test_collision_spatial_hash(self):
        sub = CollisionMatrixSubsystem()
        buckets = sub.evaluate_spatial_hash_bucket_0(10, 10, 1)
        self.assertEqual(len(buckets), 9)
