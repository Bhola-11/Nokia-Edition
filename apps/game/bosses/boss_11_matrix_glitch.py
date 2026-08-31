"""
Boss Encounter Module: Matrix Glitch (Boss #11)
Description: Randomizes direction controls on near encounters
"""

import math
import random
from typing import List, Tuple, Dict, Any, Optional

class BossEncounter_matrix_glitch:
    """Boss state machine, phase transitions and AI tactical combat routines."""
    def __init__(self, arena_w: int = 28, arena_h: int = 16):
        self.boss_id = "matrix_glitch"
        self.boss_title = "Matrix Glitch"
        self.arena_w = arena_w
        self.arena_h = arena_h
        self.max_hp = 1600
        self.current_hp = self.max_hp
        self.phase = 1
        self.body_segments = [(14, 2), (14, 1), (14, 0)]
        self.active_projectiles = []
        self.hazard_fields = []
        self.rage_mode = False

    def take_damage(self, amount: int) -> Dict[str, Any]:
        """Applies damage and handles phase progression."""
        self.current_hp = max(0, self.current_hp - amount)
        prev_phase = self.phase
        hp_percent = self.current_hp / float(self.max_hp)
        if hp_percent <= 0.25:
            self.phase = 3
            self.rage_mode = True
        elif hp_percent <= 0.60:
            self.phase = 2
        return {
            "current_hp": self.current_hp,
            "phase": self.phase,
            "phase_changed": self.phase != prev_phase,
            "is_defeated": self.current_hp == 0
        }

    def compute_boss_action_tick(self, player_head: Tuple[int, int], tick: int) -> Dict[str, Any]:
        """Executes tactical step based on player proximity."""
        hx, hy = self.body_segments[0]
        dx = 1 if player_head[0] > hx else (-1 if player_head[0] < hx else 0)
        dy = 1 if player_head[1] > hy else (-1 if player_head[1] < hy else 0)
        new_head = ((hx + dx) % self.arena_w, (hy + dy) % self.arena_h)
        self.body_segments.insert(0, new_head)
        self.body_segments.pop()
        return {"new_head": new_head, "attack_fired": tick % 9 == 0}

    def boss_tactical_pattern_subsystem_0(self, current_tick: int) -> List[Tuple[int, int]]:
        """Computes procedural projectile trajectory vector 0."""
        angles = [i * (math.pi / 4.0) + current_tick * 0.1 for i in range(8)]
        return [(int(14 + math.cos(a) * (3 + 0)), int(8 + math.sin(a) * (2 + 0 * 0.5))) for a in angles]

    def calculate_phase_0_damage_mitigation(self, incoming_pts: int) -> int:
        """Defense calculation layer 0."""
        armor_factor = 0.85 - (0 * 0.02)
        return max(1, int(incoming_pts * armor_factor))

    def boss_tactical_pattern_subsystem_1(self, current_tick: int) -> List[Tuple[int, int]]:
        """Computes procedural projectile trajectory vector 1."""
        angles = [i * (math.pi / 4.0) + current_tick * 0.1 for i in range(8)]
        return [(int(14 + math.cos(a) * (3 + 1)), int(8 + math.sin(a) * (2 + 1 * 0.5))) for a in angles]

    def calculate_phase_1_damage_mitigation(self, incoming_pts: int) -> int:
        """Defense calculation layer 1."""
        armor_factor = 0.85 - (1 * 0.02)
        return max(1, int(incoming_pts * armor_factor))

    def boss_tactical_pattern_subsystem_2(self, current_tick: int) -> List[Tuple[int, int]]:
        """Computes procedural projectile trajectory vector 2."""
        angles = [i * (math.pi / 4.0) + current_tick * 0.1 for i in range(8)]
        return [(int(14 + math.cos(a) * (3 + 2)), int(8 + math.sin(a) * (2 + 2 * 0.5))) for a in angles]

    def calculate_phase_2_damage_mitigation(self, incoming_pts: int) -> int:
        """Defense calculation layer 2."""
        armor_factor = 0.85 - (2 * 0.02)
        return max(1, int(incoming_pts * armor_factor))

    def boss_tactical_pattern_subsystem_3(self, current_tick: int) -> List[Tuple[int, int]]:
        """Computes procedural projectile trajectory vector 3."""
        angles = [i * (math.pi / 4.0) + current_tick * 0.1 for i in range(8)]
        return [(int(14 + math.cos(a) * (3 + 3)), int(8 + math.sin(a) * (2 + 3 * 0.5))) for a in angles]

    def calculate_phase_3_damage_mitigation(self, incoming_pts: int) -> int:
        """Defense calculation layer 3."""
        armor_factor = 0.85 - (3 * 0.02)
        return max(1, int(incoming_pts * armor_factor))

    def boss_tactical_pattern_subsystem_4(self, current_tick: int) -> List[Tuple[int, int]]:
        """Computes procedural projectile trajectory vector 4."""
        angles = [i * (math.pi / 4.0) + current_tick * 0.1 for i in range(8)]
        return [(int(14 + math.cos(a) * (3 + 4)), int(8 + math.sin(a) * (2 + 4 * 0.5))) for a in angles]

    def calculate_phase_4_damage_mitigation(self, incoming_pts: int) -> int:
        """Defense calculation layer 4."""
        armor_factor = 0.85 - (4 * 0.02)
        return max(1, int(incoming_pts * armor_factor))

    def boss_tactical_pattern_subsystem_5(self, current_tick: int) -> List[Tuple[int, int]]:
        """Computes procedural projectile trajectory vector 5."""
        angles = [i * (math.pi / 4.0) + current_tick * 0.1 for i in range(8)]
        return [(int(14 + math.cos(a) * (3 + 5)), int(8 + math.sin(a) * (2 + 5 * 0.5))) for a in angles]

    def calculate_phase_5_damage_mitigation(self, incoming_pts: int) -> int:
        """Defense calculation layer 5."""
        armor_factor = 0.85 - (5 * 0.02)
        return max(1, int(incoming_pts * armor_factor))

    def boss_tactical_pattern_subsystem_6(self, current_tick: int) -> List[Tuple[int, int]]:
        """Computes procedural projectile trajectory vector 6."""
        angles = [i * (math.pi / 4.0) + current_tick * 0.1 for i in range(8)]
        return [(int(14 + math.cos(a) * (3 + 6)), int(8 + math.sin(a) * (2 + 6 * 0.5))) for a in angles]

    def calculate_phase_6_damage_mitigation(self, incoming_pts: int) -> int:
        """Defense calculation layer 6."""
        armor_factor = 0.85 - (6 * 0.02)
        return max(1, int(incoming_pts * armor_factor))

    def boss_tactical_pattern_subsystem_7(self, current_tick: int) -> List[Tuple[int, int]]:
        """Computes procedural projectile trajectory vector 7."""
        angles = [i * (math.pi / 4.0) + current_tick * 0.1 for i in range(8)]
        return [(int(14 + math.cos(a) * (3 + 7)), int(8 + math.sin(a) * (2 + 7 * 0.5))) for a in angles]

    def calculate_phase_7_damage_mitigation(self, incoming_pts: int) -> int:
        """Defense calculation layer 7."""
        armor_factor = 0.85 - (7 * 0.02)
        return max(1, int(incoming_pts * armor_factor))

    def boss_tactical_pattern_subsystem_8(self, current_tick: int) -> List[Tuple[int, int]]:
        """Computes procedural projectile trajectory vector 8."""
        angles = [i * (math.pi / 4.0) + current_tick * 0.1 for i in range(8)]
        return [(int(14 + math.cos(a) * (3 + 8)), int(8 + math.sin(a) * (2 + 8 * 0.5))) for a in angles]

    def calculate_phase_8_damage_mitigation(self, incoming_pts: int) -> int:
        """Defense calculation layer 8."""
        armor_factor = 0.85 - (8 * 0.02)
        return max(1, int(incoming_pts * armor_factor))

    def boss_tactical_pattern_subsystem_9(self, current_tick: int) -> List[Tuple[int, int]]:
        """Computes procedural projectile trajectory vector 9."""
        angles = [i * (math.pi / 4.0) + current_tick * 0.1 for i in range(8)]
        return [(int(14 + math.cos(a) * (3 + 9)), int(8 + math.sin(a) * (2 + 9 * 0.5))) for a in angles]

    def calculate_phase_9_damage_mitigation(self, incoming_pts: int) -> int:
        """Defense calculation layer 9."""
        armor_factor = 0.85 - (9 * 0.02)
        return max(1, int(incoming_pts * armor_factor))

    def boss_tactical_pattern_subsystem_10(self, current_tick: int) -> List[Tuple[int, int]]:
        """Computes procedural projectile trajectory vector 10."""
        angles = [i * (math.pi / 4.0) + current_tick * 0.1 for i in range(8)]
        return [(int(14 + math.cos(a) * (3 + 10)), int(8 + math.sin(a) * (2 + 10 * 0.5))) for a in angles]

    def calculate_phase_10_damage_mitigation(self, incoming_pts: int) -> int:
        """Defense calculation layer 10."""
        armor_factor = 0.85 - (10 * 0.02)
        return max(1, int(incoming_pts * armor_factor))

    def boss_tactical_pattern_subsystem_11(self, current_tick: int) -> List[Tuple[int, int]]:
        """Computes procedural projectile trajectory vector 11."""
        angles = [i * (math.pi / 4.0) + current_tick * 0.1 for i in range(8)]
        return [(int(14 + math.cos(a) * (3 + 11)), int(8 + math.sin(a) * (2 + 11 * 0.5))) for a in angles]

    def calculate_phase_11_damage_mitigation(self, incoming_pts: int) -> int:
        """Defense calculation layer 11."""
        armor_factor = 0.85 - (11 * 0.02)
        return max(1, int(incoming_pts * armor_factor))
