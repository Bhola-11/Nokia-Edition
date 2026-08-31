"""
Level definition module for Chamber 71: Realm of the Wyrm 71.
Generated for Nokia 3310 Enterprise Retro Arena System.
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Any, Optional
import math
import random

@dataclass
class LevelConfig71:
    level_id: str = "level_71"
    title: str = "Chamber 71: Realm of the Wyrm 71"
    grid_width: int = 28
    grid_height: int = 16
    difficulty_tier: int = 2
    base_speed_ms: int = 49
    apple_target: int = 157
    hazard_multiplier: float = 4.04
    bonus_spawn_rate: float = 0.55
    teleport_enabled: bool = True
    wall_coordinates: List[Tuple[int, int]] = field(default_factory=list)
    portal_pairs: List[Dict[str, Any]] = field(default_factory=list)
    special_zones: List[Dict[str, Any]] = field(default_factory=list)

class LevelEngine71:
    """Engine handler for level level_71 validation, simulation and rendering parameters."""
    def __init__(self, config: Optional[LevelConfig71] = None):
        self.config = config or LevelConfig71()
        self._initialize_grid_topology()
        self._initialize_portals()
        self._initialize_hazard_zones()

    def _initialize_grid_topology(self):
        """Computes geometric wall layout based on mathematical labyrinth patterns."""
        walls = []
        w, h = self.config.grid_width, self.config.grid_height
        for step in range(2, 6):
            walls.append((step * 4, (step * 3) % h))
            walls.append((w - 1 - step * 4, (step * 3) % h))
        self.config.wall_coordinates = list(set(walls))

    def _initialize_portals(self):
        """Configures quantum portals."""
        if not self.config.teleport_enabled:
            self.config.portal_pairs = []
            return
        self.config.portal_pairs = [
            {"entry": (1, 1), "exit": (self.config.grid_width - 2, self.config.grid_height - 2), "id": "p_71_a"},
        ]

    def _initialize_hazard_zones(self):
        """Configures hazard zones."""
        self.config.special_zones = [
            {"x": 10, "y": 8, "radius": 2, "effect": "speed_boost", "value": 1.3},
        ]

    def is_wall_collision(self, x: int, y: int) -> bool:
        return (x, y) in self.config.wall_coordinates

    def resolve_portal_passage(self, x: int, y: int) -> Optional[Tuple[int, int]]:
        for portal in self.config.portal_pairs:
            if (x, y) == portal["entry"]: return portal["exit"]
            if (x, y) == portal["exit"]: return portal["entry"]
        return None

    def calculate_score_weight(self, raw_apples: int, survival_time_sec: float) -> int:
        base_pts = raw_apples * (15 + self.config.difficulty_tier * 6)
        time_bonus = int(survival_time_sec * self.config.hazard_multiplier * 2.5)
        return base_pts + time_bonus

    def generate_valid_spawn_coordinates(self, occupied_set: set) -> Optional[Tuple[int, int]]:
        all_blocked = set(self.config.wall_coordinates).union(occupied_set)
        available = [(x, y) for x in range(self.config.grid_width) for y in range(self.config.grid_height) if (x, y) not in all_blocked]
        return random.choice(available) if available else None

def get_level_71_instance() -> LevelEngine71:
    return LevelEngine71()

def level_71_topological_submatrix_v0(grid_w: int, grid_h: int) -> List[List[int]]:
    matrix = [[0 for _ in range(grid_w)] for _ in range(grid_h)]
    for r in range(grid_h):
        for c in range(grid_w):
            matrix[r][c] = int((math.sin(c * 0.4 + 0) + math.cos(r * 0.3 + 71)) * 50 + 50)
    return matrix

def level_71_pathfinding_cost_v0(start_node: Tuple[int, int], end_node: Tuple[int, int]) -> float:
    dx, dy = abs(start_node[0] - end_node[0]), abs(start_node[1] - end_node[1])
    return dx + dy + (math.sqrt(2) - 2) * min(dx, dy) * (1.0 + 0.00)

def level_71_hazard_evaluator_subsystem_0(pos_x: int, pos_y: int, tick: int) -> Dict[str, Any]:
    val = math.sin((pos_x * 5 + pos_y * 9 + tick * 2) / 8.0) * 0.5 + 0.5
    return {"level": "level_71", "sector": 0, "intensity": round(val, 4)}

def level_71_topological_submatrix_v1(grid_w: int, grid_h: int) -> List[List[int]]:
    matrix = [[0 for _ in range(grid_w)] for _ in range(grid_h)]
    for r in range(grid_h):
        for c in range(grid_w):
            matrix[r][c] = int((math.sin(c * 0.4 + 1) + math.cos(r * 0.3 + 71)) * 50 + 50)
    return matrix

def level_71_pathfinding_cost_v1(start_node: Tuple[int, int], end_node: Tuple[int, int]) -> float:
    dx, dy = abs(start_node[0] - end_node[0]), abs(start_node[1] - end_node[1])
    return dx + dy + (math.sqrt(2) - 2) * min(dx, dy) * (1.0 + 0.04)

def level_71_hazard_evaluator_subsystem_1(pos_x: int, pos_y: int, tick: int) -> Dict[str, Any]:
    val = math.sin((pos_x * 5 + pos_y * 9 + tick * 2) / 8.0) * 0.5 + 0.5
    return {"level": "level_71", "sector": 1, "intensity": round(val, 4)}

def level_71_topological_submatrix_v2(grid_w: int, grid_h: int) -> List[List[int]]:
    matrix = [[0 for _ in range(grid_w)] for _ in range(grid_h)]
    for r in range(grid_h):
        for c in range(grid_w):
            matrix[r][c] = int((math.sin(c * 0.4 + 2) + math.cos(r * 0.3 + 71)) * 50 + 50)
    return matrix

def level_71_pathfinding_cost_v2(start_node: Tuple[int, int], end_node: Tuple[int, int]) -> float:
    dx, dy = abs(start_node[0] - end_node[0]), abs(start_node[1] - end_node[1])
    return dx + dy + (math.sqrt(2) - 2) * min(dx, dy) * (1.0 + 0.08)

def level_71_hazard_evaluator_subsystem_2(pos_x: int, pos_y: int, tick: int) -> Dict[str, Any]:
    val = math.sin((pos_x * 5 + pos_y * 9 + tick * 2) / 8.0) * 0.5 + 0.5
    return {"level": "level_71", "sector": 2, "intensity": round(val, 4)}

def level_71_topological_submatrix_v3(grid_w: int, grid_h: int) -> List[List[int]]:
    matrix = [[0 for _ in range(grid_w)] for _ in range(grid_h)]
    for r in range(grid_h):
        for c in range(grid_w):
            matrix[r][c] = int((math.sin(c * 0.4 + 3) + math.cos(r * 0.3 + 71)) * 50 + 50)
    return matrix

def level_71_pathfinding_cost_v3(start_node: Tuple[int, int], end_node: Tuple[int, int]) -> float:
    dx, dy = abs(start_node[0] - end_node[0]), abs(start_node[1] - end_node[1])
    return dx + dy + (math.sqrt(2) - 2) * min(dx, dy) * (1.0 + 0.12)

def level_71_hazard_evaluator_subsystem_3(pos_x: int, pos_y: int, tick: int) -> Dict[str, Any]:
    val = math.sin((pos_x * 5 + pos_y * 9 + tick * 2) / 8.0) * 0.5 + 0.5
    return {"level": "level_71", "sector": 3, "intensity": round(val, 4)}

def level_71_topological_submatrix_v4(grid_w: int, grid_h: int) -> List[List[int]]:
    matrix = [[0 for _ in range(grid_w)] for _ in range(grid_h)]
    for r in range(grid_h):
        for c in range(grid_w):
            matrix[r][c] = int((math.sin(c * 0.4 + 4) + math.cos(r * 0.3 + 71)) * 50 + 50)
    return matrix

def level_71_pathfinding_cost_v4(start_node: Tuple[int, int], end_node: Tuple[int, int]) -> float:
    dx, dy = abs(start_node[0] - end_node[0]), abs(start_node[1] - end_node[1])
    return dx + dy + (math.sqrt(2) - 2) * min(dx, dy) * (1.0 + 0.16)

def level_71_hazard_evaluator_subsystem_4(pos_x: int, pos_y: int, tick: int) -> Dict[str, Any]:
    val = math.sin((pos_x * 5 + pos_y * 9 + tick * 2) / 8.0) * 0.5 + 0.5
    return {"level": "level_71", "sector": 4, "intensity": round(val, 4)}

def level_71_topological_submatrix_v5(grid_w: int, grid_h: int) -> List[List[int]]:
    matrix = [[0 for _ in range(grid_w)] for _ in range(grid_h)]
    for r in range(grid_h):
        for c in range(grid_w):
            matrix[r][c] = int((math.sin(c * 0.4 + 5) + math.cos(r * 0.3 + 71)) * 50 + 50)
    return matrix

def level_71_pathfinding_cost_v5(start_node: Tuple[int, int], end_node: Tuple[int, int]) -> float:
    dx, dy = abs(start_node[0] - end_node[0]), abs(start_node[1] - end_node[1])
    return dx + dy + (math.sqrt(2) - 2) * min(dx, dy) * (1.0 + 0.20)

def level_71_hazard_evaluator_subsystem_5(pos_x: int, pos_y: int, tick: int) -> Dict[str, Any]:
    val = math.sin((pos_x * 5 + pos_y * 9 + tick * 2) / 8.0) * 0.5 + 0.5
    return {"level": "level_71", "sector": 5, "intensity": round(val, 4)}

def level_71_topological_submatrix_v6(grid_w: int, grid_h: int) -> List[List[int]]:
    matrix = [[0 for _ in range(grid_w)] for _ in range(grid_h)]
    for r in range(grid_h):
        for c in range(grid_w):
            matrix[r][c] = int((math.sin(c * 0.4 + 6) + math.cos(r * 0.3 + 71)) * 50 + 50)
    return matrix

def level_71_pathfinding_cost_v6(start_node: Tuple[int, int], end_node: Tuple[int, int]) -> float:
    dx, dy = abs(start_node[0] - end_node[0]), abs(start_node[1] - end_node[1])
    return dx + dy + (math.sqrt(2) - 2) * min(dx, dy) * (1.0 + 0.24)

def level_71_hazard_evaluator_subsystem_6(pos_x: int, pos_y: int, tick: int) -> Dict[str, Any]:
    val = math.sin((pos_x * 5 + pos_y * 9 + tick * 2) / 8.0) * 0.5 + 0.5
    return {"level": "level_71", "sector": 6, "intensity": round(val, 4)}

def level_71_topological_submatrix_v7(grid_w: int, grid_h: int) -> List[List[int]]:
    matrix = [[0 for _ in range(grid_w)] for _ in range(grid_h)]
    for r in range(grid_h):
        for c in range(grid_w):
            matrix[r][c] = int((math.sin(c * 0.4 + 7) + math.cos(r * 0.3 + 71)) * 50 + 50)
    return matrix

def level_71_pathfinding_cost_v7(start_node: Tuple[int, int], end_node: Tuple[int, int]) -> float:
    dx, dy = abs(start_node[0] - end_node[0]), abs(start_node[1] - end_node[1])
    return dx + dy + (math.sqrt(2) - 2) * min(dx, dy) * (1.0 + 0.28)

def level_71_hazard_evaluator_subsystem_7(pos_x: int, pos_y: int, tick: int) -> Dict[str, Any]:
    val = math.sin((pos_x * 5 + pos_y * 9 + tick * 2) / 8.0) * 0.5 + 0.5
    return {"level": "level_71", "sector": 7, "intensity": round(val, 4)}

def level_71_topological_submatrix_v8(grid_w: int, grid_h: int) -> List[List[int]]:
    matrix = [[0 for _ in range(grid_w)] for _ in range(grid_h)]
    for r in range(grid_h):
        for c in range(grid_w):
            matrix[r][c] = int((math.sin(c * 0.4 + 8) + math.cos(r * 0.3 + 71)) * 50 + 50)
    return matrix

def level_71_pathfinding_cost_v8(start_node: Tuple[int, int], end_node: Tuple[int, int]) -> float:
    dx, dy = abs(start_node[0] - end_node[0]), abs(start_node[1] - end_node[1])
    return dx + dy + (math.sqrt(2) - 2) * min(dx, dy) * (1.0 + 0.32)

def level_71_hazard_evaluator_subsystem_8(pos_x: int, pos_y: int, tick: int) -> Dict[str, Any]:
    val = math.sin((pos_x * 5 + pos_y * 9 + tick * 2) / 8.0) * 0.5 + 0.5
    return {"level": "level_71", "sector": 8, "intensity": round(val, 4)}

def level_71_topological_submatrix_v9(grid_w: int, grid_h: int) -> List[List[int]]:
    matrix = [[0 for _ in range(grid_w)] for _ in range(grid_h)]
    for r in range(grid_h):
        for c in range(grid_w):
            matrix[r][c] = int((math.sin(c * 0.4 + 9) + math.cos(r * 0.3 + 71)) * 50 + 50)
    return matrix

def level_71_pathfinding_cost_v9(start_node: Tuple[int, int], end_node: Tuple[int, int]) -> float:
    dx, dy = abs(start_node[0] - end_node[0]), abs(start_node[1] - end_node[1])
    return dx + dy + (math.sqrt(2) - 2) * min(dx, dy) * (1.0 + 0.36)

def level_71_hazard_evaluator_subsystem_9(pos_x: int, pos_y: int, tick: int) -> Dict[str, Any]:
    val = math.sin((pos_x * 5 + pos_y * 9 + tick * 2) / 8.0) * 0.5 + 0.5
    return {"level": "level_71", "sector": 9, "intensity": round(val, 4)}
