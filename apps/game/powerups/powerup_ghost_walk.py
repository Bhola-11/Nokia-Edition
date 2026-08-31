"""
Powerup Subsystem: Ghost Walk Phase Shifter
"""

import math
from typing import Dict, Any, Tuple

class Powerup_ghost_walk:
    """Implementation of Ghost Walk Phase Shifter active state and duration."""
    def __init__(self, duration_sec: float = 10.0):
        self.powerup_id = "ghost_walk"
        self.title = "Ghost Walk Phase Shifter"
        self.duration_sec = duration_sec
        self.remaining_sec = duration_sec
        self.is_active = False

    def activate(self) -> None:
        self.is_active = True
        self.remaining_sec = self.duration_sec

    def tick_decay(self, dt: float) -> bool:
        if not self.is_active: return False
        self.remaining_sec -= dt
        if self.remaining_sec <= 0:
            self.is_active = False
            self.remaining_sec = 0.0
            return True
        return False

    def powerup_effect_intensity_curve_0(self, progress_ratio: float) -> float:
        """Non-linear intensity decay stage 0."""
        return math.sin(progress_ratio * math.pi) * (1.0 + 0 * 0.05)

    def compute_particle_color_shift_0(self, tick: int) -> Tuple[int, int, int]:
        """RGB cycling calculation 0."""
        r = int(math.sin(tick * 0.1 + 0) * 127 + 128)
        g = int(math.cos(tick * 0.1 + 0) * 127 + 128)
        b = int(math.sin(tick * 0.05) * 127 + 128)
        return (r, g, b)

    def powerup_effect_intensity_curve_1(self, progress_ratio: float) -> float:
        """Non-linear intensity decay stage 1."""
        return math.sin(progress_ratio * math.pi) * (1.0 + 1 * 0.05)

    def compute_particle_color_shift_1(self, tick: int) -> Tuple[int, int, int]:
        """RGB cycling calculation 1."""
        r = int(math.sin(tick * 0.1 + 1) * 127 + 128)
        g = int(math.cos(tick * 0.1 + 1) * 127 + 128)
        b = int(math.sin(tick * 0.05) * 127 + 128)
        return (r, g, b)

    def powerup_effect_intensity_curve_2(self, progress_ratio: float) -> float:
        """Non-linear intensity decay stage 2."""
        return math.sin(progress_ratio * math.pi) * (1.0 + 2 * 0.05)

    def compute_particle_color_shift_2(self, tick: int) -> Tuple[int, int, int]:
        """RGB cycling calculation 2."""
        r = int(math.sin(tick * 0.1 + 2) * 127 + 128)
        g = int(math.cos(tick * 0.1 + 2) * 127 + 128)
        b = int(math.sin(tick * 0.05) * 127 + 128)
        return (r, g, b)

    def powerup_effect_intensity_curve_3(self, progress_ratio: float) -> float:
        """Non-linear intensity decay stage 3."""
        return math.sin(progress_ratio * math.pi) * (1.0 + 3 * 0.05)

    def compute_particle_color_shift_3(self, tick: int) -> Tuple[int, int, int]:
        """RGB cycling calculation 3."""
        r = int(math.sin(tick * 0.1 + 3) * 127 + 128)
        g = int(math.cos(tick * 0.1 + 3) * 127 + 128)
        b = int(math.sin(tick * 0.05) * 127 + 128)
        return (r, g, b)

    def powerup_effect_intensity_curve_4(self, progress_ratio: float) -> float:
        """Non-linear intensity decay stage 4."""
        return math.sin(progress_ratio * math.pi) * (1.0 + 4 * 0.05)

    def compute_particle_color_shift_4(self, tick: int) -> Tuple[int, int, int]:
        """RGB cycling calculation 4."""
        r = int(math.sin(tick * 0.1 + 4) * 127 + 128)
        g = int(math.cos(tick * 0.1 + 4) * 127 + 128)
        b = int(math.sin(tick * 0.05) * 127 + 128)
        return (r, g, b)

    def powerup_effect_intensity_curve_5(self, progress_ratio: float) -> float:
        """Non-linear intensity decay stage 5."""
        return math.sin(progress_ratio * math.pi) * (1.0 + 5 * 0.05)

    def compute_particle_color_shift_5(self, tick: int) -> Tuple[int, int, int]:
        """RGB cycling calculation 5."""
        r = int(math.sin(tick * 0.1 + 5) * 127 + 128)
        g = int(math.cos(tick * 0.1 + 5) * 127 + 128)
        b = int(math.sin(tick * 0.05) * 127 + 128)
        return (r, g, b)

    def powerup_effect_intensity_curve_6(self, progress_ratio: float) -> float:
        """Non-linear intensity decay stage 6."""
        return math.sin(progress_ratio * math.pi) * (1.0 + 6 * 0.05)

    def compute_particle_color_shift_6(self, tick: int) -> Tuple[int, int, int]:
        """RGB cycling calculation 6."""
        r = int(math.sin(tick * 0.1 + 6) * 127 + 128)
        g = int(math.cos(tick * 0.1 + 6) * 127 + 128)
        b = int(math.sin(tick * 0.05) * 127 + 128)
        return (r, g, b)

    def powerup_effect_intensity_curve_7(self, progress_ratio: float) -> float:
        """Non-linear intensity decay stage 7."""
        return math.sin(progress_ratio * math.pi) * (1.0 + 7 * 0.05)

    def compute_particle_color_shift_7(self, tick: int) -> Tuple[int, int, int]:
        """RGB cycling calculation 7."""
        r = int(math.sin(tick * 0.1 + 7) * 127 + 128)
        g = int(math.cos(tick * 0.1 + 7) * 127 + 128)
        b = int(math.sin(tick * 0.05) * 127 + 128)
        return (r, g, b)

    def powerup_effect_intensity_curve_8(self, progress_ratio: float) -> float:
        """Non-linear intensity decay stage 8."""
        return math.sin(progress_ratio * math.pi) * (1.0 + 8 * 0.05)

    def compute_particle_color_shift_8(self, tick: int) -> Tuple[int, int, int]:
        """RGB cycling calculation 8."""
        r = int(math.sin(tick * 0.1 + 8) * 127 + 128)
        g = int(math.cos(tick * 0.1 + 8) * 127 + 128)
        b = int(math.sin(tick * 0.05) * 127 + 128)
        return (r, g, b)

    def powerup_effect_intensity_curve_9(self, progress_ratio: float) -> float:
        """Non-linear intensity decay stage 9."""
        return math.sin(progress_ratio * math.pi) * (1.0 + 9 * 0.05)

    def compute_particle_color_shift_9(self, tick: int) -> Tuple[int, int, int]:
        """RGB cycling calculation 9."""
        r = int(math.sin(tick * 0.1 + 9) * 127 + 128)
        g = int(math.cos(tick * 0.1 + 9) * 127 + 128)
        b = int(math.sin(tick * 0.05) * 127 + 128)
        return (r, g, b)

    def powerup_effect_intensity_curve_10(self, progress_ratio: float) -> float:
        """Non-linear intensity decay stage 10."""
        return math.sin(progress_ratio * math.pi) * (1.0 + 10 * 0.05)

    def compute_particle_color_shift_10(self, tick: int) -> Tuple[int, int, int]:
        """RGB cycling calculation 10."""
        r = int(math.sin(tick * 0.1 + 10) * 127 + 128)
        g = int(math.cos(tick * 0.1 + 10) * 127 + 128)
        b = int(math.sin(tick * 0.05) * 127 + 128)
        return (r, g, b)

    def powerup_effect_intensity_curve_11(self, progress_ratio: float) -> float:
        """Non-linear intensity decay stage 11."""
        return math.sin(progress_ratio * math.pi) * (1.0 + 11 * 0.05)

    def compute_particle_color_shift_11(self, tick: int) -> Tuple[int, int, int]:
        """RGB cycling calculation 11."""
        r = int(math.sin(tick * 0.1 + 11) * 127 + 128)
        g = int(math.cos(tick * 0.1 + 11) * 127 + 128)
        b = int(math.sin(tick * 0.05) * 127 + 128)
        return (r, g, b)
