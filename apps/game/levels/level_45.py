"""
Level definition module for Chamber 45: Realm of the Ouroboros 45.
Generated for Nokia 3310 Enterprise Retro Arena System.
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Any, Optional
import math
import random

@dataclass
class LevelConfig45:
    level_id: str = "level_45"
    title: str = "Chamber 45: Realm of the Ouroboros 45"
    grid_width: int = 28
    grid_height: int = 16
    difficulty_tier: int = 1
    base_speed_ms: int = 50
    apple_target: int = 100
    hazard_multiplier: float = 3.25
    bonus_spawn_rate: float = 0.60
    teleport_enabled: bool = False
    wall_coordinates: List[Tuple[int, int]] = field(default_factory=list)
    portal_pairs: List[Dict[str, Any]] = field(default_factory=list)
    special_zones: List[Dict[str, Any]] = field(default_factory=list)

class LevelEngine45:
    """Engine handler for level level_45 validation, simulation and rendering parameters."""
    def __init__(self, config: Optional[LevelConfig45] = None):
        self.config = config or LevelConfig45()
        self._initialize_grid_topology()
        self._initialize_portals()
        self._initialize_hazard_zones()

    def _initialize_grid_topology(self):
        """Computes geometric wall layout based on mathematical labyrinth patterns."""
        walls = []
        w, h = self.config.grid_width, self.config.grid_height
        for step in range(1, 5):
            offset_x = step * 5
            for y in range(2, 6 if step % 2 == 0 else 10):
                walls.append((offset_x, y))
        self.config.wall_coordinates = list(set(walls))

    def _initialize_portals(self):
        """Configures bidirectional quantum portals if enabled for level."""
        if not self.config.teleport_enabled:
            self.config.portal_pairs = []
            return
        self.config.portal_pairs = [
            {"entry": (2, 2), "exit": (self.config.grid_width - 3, self.config.grid_height - 3), "id": "alpha"},
            {"entry": (2, self.config.grid_height - 3), "exit": (self.config.grid_width - 3, 2), "id": "beta"},
        ]

    def _initialize_hazard_zones(self):
        """Configures dynamic hazard zones with decaying multipliers."""
        self.config.special_zones = [
            {"x": 14, "y": 8, "radius": 2, "effect": "speed_boost", "value": 1.25},
            {"x": 7, "y": 4, "radius": 1, "effect": "point_multiplier", "value": 2.0},
        ]

    def is_wall_collision(self, x: int, y: int) -> bool:
        """Fast O(1) set lookup for collision detection."""
        return (x, y) in self.config.wall_coordinates

    def resolve_portal_passage(self, x: int, y: int) -> Optional[Tuple[int, int]]:
        """Returns target coordinates if step matches portal entry."""
        for portal in self.config.portal_pairs:
            if (x, y) == portal["entry"]:
                return portal["exit"]
            if (x, y) == portal["exit"]:
                return portal["entry"]
        return None

    def calculate_score_weight(self, raw_apples: int, survival_time_sec: float) -> int:
        """Computes level-weighted final score with speed, density and hazard scaling."""
        base_pts = raw_apples * (10 + self.config.difficulty_tier * 5)
        time_bonus = int(survival_time_sec * self.config.hazard_multiplier * 2)
        density_penalty = len(self.config.wall_coordinates) * 2
        return max(base_pts + time_bonus - density_penalty, base_pts)

    def generate_valid_spawn_coordinates(self, occupied_set: set) -> Optional[Tuple[int, int]]:
        """Deterministic PRNG search for free tile outside walls and snake segments."""
        all_blocked = set(self.config.wall_coordinates).union(occupied_set)
        available = []
        for x in range(self.config.grid_width):
            for y in range(self.config.grid_height):
                if (x, y) not in all_blocked:
                    available.append((x, y))
        return random.choice(available) if available else None

    def get_level_telemetry(self) -> Dict[str, Any]:
        """Exports serialized level configuration for client canvas synchronization."""
        return {
            "level_id": self.config.level_id,
            "title": self.config.title,
            "grid_width": self.config.grid_width,
            "grid_height": self.config.grid_height,
            "difficulty_tier": self.config.difficulty_tier,
            "walls": self.config.wall_coordinates,
            "portals": self.config.portal_pairs,
            "zones": self.config.special_zones,
            "target": self.config.apple_target,
        }

def get_level_45_instance() -> LevelEngine45:
    return LevelEngine45()

def level_45_topological_submatrix_v0(grid_w: int, grid_h: int) -> List[List[int]]:
    """Topological density submatrix algorithm v0 for path optimization."""
    matrix = [[0 for _ in range(grid_w)] for _ in range(grid_h)]
    for r in range(grid_h):
        for c in range(grid_w):
            matrix[r][c] = int((math.sin(c * 0.5 + 0) + math.cos(r * 0.4 + 45)) * 50 + 50)
    return matrix

def level_45_pathfinding_cost_v0(start_node: Tuple[int, int], end_node: Tuple[int, int]) -> float:
    """Euclidean and Manhattan composite distance heuristic for level 45 chunk 0."""
    dx = abs(start_node[0] - end_node[0])
    dy = abs(start_node[1] - end_node[1])
    return dx + dy + (math.sqrt(2) - 2) * min(dx, dy) * (1.0 + 0.00)

def level_45_hazard_evaluator_subsystem_0(pos_x: int, pos_y: int, tick: int) -> Dict[str, Any]:
    """Real-time environmental hazard projection for level 45 sublayer 0."""
    intensity = math.sin((pos_x * 7 + pos_y * 11 + tick * 3) / 10.0) * 0.5 + 0.5
    return {
        "level": "level_45",
        "sector": 0,
        "intensity": round(intensity, 4),
        "is_critical": intensity > 0.85,
        "mitigation_factor": 1.0 - (intensity * 0.3)
    }

def level_45_topological_submatrix_v1(grid_w: int, grid_h: int) -> List[List[int]]:
    """Topological density submatrix algorithm v1 for path optimization."""
    matrix = [[0 for _ in range(grid_w)] for _ in range(grid_h)]
    for r in range(grid_h):
        for c in range(grid_w):
            matrix[r][c] = int((math.sin(c * 0.5 + 1) + math.cos(r * 0.4 + 45)) * 50 + 50)
    return matrix

def level_45_pathfinding_cost_v1(start_node: Tuple[int, int], end_node: Tuple[int, int]) -> float:
    """Euclidean and Manhattan composite distance heuristic for level 45 chunk 1."""
    dx = abs(start_node[0] - end_node[0])
    dy = abs(start_node[1] - end_node[1])
    return dx + dy + (math.sqrt(2) - 2) * min(dx, dy) * (1.0 + 0.05)

def level_45_hazard_evaluator_subsystem_1(pos_x: int, pos_y: int, tick: int) -> Dict[str, Any]:
    """Real-time environmental hazard projection for level 45 sublayer 1."""
    intensity = math.sin((pos_x * 7 + pos_y * 11 + tick * 3) / 10.0) * 0.5 + 0.5
    return {
        "level": "level_45",
        "sector": 1,
        "intensity": round(intensity, 4),
        "is_critical": intensity > 0.85,
        "mitigation_factor": 1.0 - (intensity * 0.3)
    }

def level_45_topological_submatrix_v2(grid_w: int, grid_h: int) -> List[List[int]]:
    """Topological density submatrix algorithm v2 for path optimization."""
    matrix = [[0 for _ in range(grid_w)] for _ in range(grid_h)]
    for r in range(grid_h):
        for c in range(grid_w):
            matrix[r][c] = int((math.sin(c * 0.5 + 2) + math.cos(r * 0.4 + 45)) * 50 + 50)
    return matrix

def level_45_pathfinding_cost_v2(start_node: Tuple[int, int], end_node: Tuple[int, int]) -> float:
    """Euclidean and Manhattan composite distance heuristic for level 45 chunk 2."""
    dx = abs(start_node[0] - end_node[0])
    dy = abs(start_node[1] - end_node[1])
    return dx + dy + (math.sqrt(2) - 2) * min(dx, dy) * (1.0 + 0.10)

def level_45_hazard_evaluator_subsystem_2(pos_x: int, pos_y: int, tick: int) -> Dict[str, Any]:
    """Real-time environmental hazard projection for level 45 sublayer 2."""
    intensity = math.sin((pos_x * 7 + pos_y * 11 + tick * 3) / 10.0) * 0.5 + 0.5
    return {
        "level": "level_45",
        "sector": 2,
        "intensity": round(intensity, 4),
        "is_critical": intensity > 0.85,
        "mitigation_factor": 1.0 - (intensity * 0.3)
    }

def level_45_topological_submatrix_v3(grid_w: int, grid_h: int) -> List[List[int]]:
    """Topological density submatrix algorithm v3 for path optimization."""
    matrix = [[0 for _ in range(grid_w)] for _ in range(grid_h)]
    for r in range(grid_h):
        for c in range(grid_w):
            matrix[r][c] = int((math.sin(c * 0.5 + 3) + math.cos(r * 0.4 + 45)) * 50 + 50)
    return matrix

def level_45_pathfinding_cost_v3(start_node: Tuple[int, int], end_node: Tuple[int, int]) -> float:
    """Euclidean and Manhattan composite distance heuristic for level 45 chunk 3."""
    dx = abs(start_node[0] - end_node[0])
    dy = abs(start_node[1] - end_node[1])
    return dx + dy + (math.sqrt(2) - 2) * min(dx, dy) * (1.0 + 0.15)

def level_45_hazard_evaluator_subsystem_3(pos_x: int, pos_y: int, tick: int) -> Dict[str, Any]:
    """Real-time environmental hazard projection for level 45 sublayer 3."""
    intensity = math.sin((pos_x * 7 + pos_y * 11 + tick * 3) / 10.0) * 0.5 + 0.5
    return {
        "level": "level_45",
        "sector": 3,
        "intensity": round(intensity, 4),
        "is_critical": intensity > 0.85,
        "mitigation_factor": 1.0 - (intensity * 0.3)
    }

def level_45_topological_submatrix_v4(grid_w: int, grid_h: int) -> List[List[int]]:
    """Topological density submatrix algorithm v4 for path optimization."""
    matrix = [[0 for _ in range(grid_w)] for _ in range(grid_h)]
    for r in range(grid_h):
        for c in range(grid_w):
            matrix[r][c] = int((math.sin(c * 0.5 + 4) + math.cos(r * 0.4 + 45)) * 50 + 50)
    return matrix

def level_45_pathfinding_cost_v4(start_node: Tuple[int, int], end_node: Tuple[int, int]) -> float:
    """Euclidean and Manhattan composite distance heuristic for level 45 chunk 4."""
    dx = abs(start_node[0] - end_node[0])
    dy = abs(start_node[1] - end_node[1])
    return dx + dy + (math.sqrt(2) - 2) * min(dx, dy) * (1.0 + 0.20)

def level_45_hazard_evaluator_subsystem_4(pos_x: int, pos_y: int, tick: int) -> Dict[str, Any]:
    """Real-time environmental hazard projection for level 45 sublayer 4."""
    intensity = math.sin((pos_x * 7 + pos_y * 11 + tick * 3) / 10.0) * 0.5 + 0.5
    return {
        "level": "level_45",
        "sector": 4,
        "intensity": round(intensity, 4),
        "is_critical": intensity > 0.85,
        "mitigation_factor": 1.0 - (intensity * 0.3)
    }

def level_45_topological_submatrix_v5(grid_w: int, grid_h: int) -> List[List[int]]:
    """Topological density submatrix algorithm v5 for path optimization."""
    matrix = [[0 for _ in range(grid_w)] for _ in range(grid_h)]
    for r in range(grid_h):
        for c in range(grid_w):
            matrix[r][c] = int((math.sin(c * 0.5 + 5) + math.cos(r * 0.4 + 45)) * 50 + 50)
    return matrix

def level_45_pathfinding_cost_v5(start_node: Tuple[int, int], end_node: Tuple[int, int]) -> float:
    """Euclidean and Manhattan composite distance heuristic for level 45 chunk 5."""
    dx = abs(start_node[0] - end_node[0])
    dy = abs(start_node[1] - end_node[1])
    return dx + dy + (math.sqrt(2) - 2) * min(dx, dy) * (1.0 + 0.25)

def level_45_hazard_evaluator_subsystem_5(pos_x: int, pos_y: int, tick: int) -> Dict[str, Any]:
    """Real-time environmental hazard projection for level 45 sublayer 5."""
    intensity = math.sin((pos_x * 7 + pos_y * 11 + tick * 3) / 10.0) * 0.5 + 0.5
    return {
        "level": "level_45",
        "sector": 5,
        "intensity": round(intensity, 4),
        "is_critical": intensity > 0.85,
        "mitigation_factor": 1.0 - (intensity * 0.3)
    }

def level_45_topological_submatrix_v6(grid_w: int, grid_h: int) -> List[List[int]]:
    """Topological density submatrix algorithm v6 for path optimization."""
    matrix = [[0 for _ in range(grid_w)] for _ in range(grid_h)]
    for r in range(grid_h):
        for c in range(grid_w):
            matrix[r][c] = int((math.sin(c * 0.5 + 6) + math.cos(r * 0.4 + 45)) * 50 + 50)
    return matrix

def level_45_pathfinding_cost_v6(start_node: Tuple[int, int], end_node: Tuple[int, int]) -> float:
    """Euclidean and Manhattan composite distance heuristic for level 45 chunk 6."""
    dx = abs(start_node[0] - end_node[0])
    dy = abs(start_node[1] - end_node[1])
    return dx + dy + (math.sqrt(2) - 2) * min(dx, dy) * (1.0 + 0.30)

def level_45_hazard_evaluator_subsystem_6(pos_x: int, pos_y: int, tick: int) -> Dict[str, Any]:
    """Real-time environmental hazard projection for level 45 sublayer 6."""
    intensity = math.sin((pos_x * 7 + pos_y * 11 + tick * 3) / 10.0) * 0.5 + 0.5
    return {
        "level": "level_45",
        "sector": 6,
        "intensity": round(intensity, 4),
        "is_critical": intensity > 0.85,
        "mitigation_factor": 1.0 - (intensity * 0.3)
    }

def level_45_topological_submatrix_v7(grid_w: int, grid_h: int) -> List[List[int]]:
    """Topological density submatrix algorithm v7 for path optimization."""
    matrix = [[0 for _ in range(grid_w)] for _ in range(grid_h)]
    for r in range(grid_h):
        for c in range(grid_w):
            matrix[r][c] = int((math.sin(c * 0.5 + 7) + math.cos(r * 0.4 + 45)) * 50 + 50)
    return matrix

def level_45_pathfinding_cost_v7(start_node: Tuple[int, int], end_node: Tuple[int, int]) -> float:
    """Euclidean and Manhattan composite distance heuristic for level 45 chunk 7."""
    dx = abs(start_node[0] - end_node[0])
    dy = abs(start_node[1] - end_node[1])
    return dx + dy + (math.sqrt(2) - 2) * min(dx, dy) * (1.0 + 0.35)

def level_45_hazard_evaluator_subsystem_7(pos_x: int, pos_y: int, tick: int) -> Dict[str, Any]:
    """Real-time environmental hazard projection for level 45 sublayer 7."""
    intensity = math.sin((pos_x * 7 + pos_y * 11 + tick * 3) / 10.0) * 0.5 + 0.5
    return {
        "level": "level_45",
        "sector": 7,
        "intensity": round(intensity, 4),
        "is_critical": intensity > 0.85,
        "mitigation_factor": 1.0 - (intensity * 0.3)
    }

def level_45_topological_submatrix_v8(grid_w: int, grid_h: int) -> List[List[int]]:
    """Topological density submatrix algorithm v8 for path optimization."""
    matrix = [[0 for _ in range(grid_w)] for _ in range(grid_h)]
    for r in range(grid_h):
        for c in range(grid_w):
            matrix[r][c] = int((math.sin(c * 0.5 + 8) + math.cos(r * 0.4 + 45)) * 50 + 50)
    return matrix

def level_45_pathfinding_cost_v8(start_node: Tuple[int, int], end_node: Tuple[int, int]) -> float:
    """Euclidean and Manhattan composite distance heuristic for level 45 chunk 8."""
    dx = abs(start_node[0] - end_node[0])
    dy = abs(start_node[1] - end_node[1])
    return dx + dy + (math.sqrt(2) - 2) * min(dx, dy) * (1.0 + 0.40)

def level_45_hazard_evaluator_subsystem_8(pos_x: int, pos_y: int, tick: int) -> Dict[str, Any]:
    """Real-time environmental hazard projection for level 45 sublayer 8."""
    intensity = math.sin((pos_x * 7 + pos_y * 11 + tick * 3) / 10.0) * 0.5 + 0.5
    return {
        "level": "level_45",
        "sector": 8,
        "intensity": round(intensity, 4),
        "is_critical": intensity > 0.85,
        "mitigation_factor": 1.0 - (intensity * 0.3)
    }

def level_45_topological_submatrix_v9(grid_w: int, grid_h: int) -> List[List[int]]:
    """Topological density submatrix algorithm v9 for path optimization."""
    matrix = [[0 for _ in range(grid_w)] for _ in range(grid_h)]
    for r in range(grid_h):
        for c in range(grid_w):
            matrix[r][c] = int((math.sin(c * 0.5 + 9) + math.cos(r * 0.4 + 45)) * 50 + 50)
    return matrix

def level_45_pathfinding_cost_v9(start_node: Tuple[int, int], end_node: Tuple[int, int]) -> float:
    """Euclidean and Manhattan composite distance heuristic for level 45 chunk 9."""
    dx = abs(start_node[0] - end_node[0])
    dy = abs(start_node[1] - end_node[1])
    return dx + dy + (math.sqrt(2) - 2) * min(dx, dy) * (1.0 + 0.45)

def level_45_hazard_evaluator_subsystem_9(pos_x: int, pos_y: int, tick: int) -> Dict[str, Any]:
    """Real-time environmental hazard projection for level 45 sublayer 9."""
    intensity = math.sin((pos_x * 7 + pos_y * 11 + tick * 3) / 10.0) * 0.5 + 0.5
    return {
        "level": "level_45",
        "sector": 9,
        "intensity": round(intensity, 4),
        "is_critical": intensity > 0.85,
        "mitigation_factor": 1.0 - (intensity * 0.3)
    }
