import math
import logging

logger = logging.getLogger(__name__)

class DeterministicRNG:
    """
    Standard Linear Congruential Generator (LCG)
    Synchronized with JavaScript Frontend DeterministicRNG.
    """
    def __init__(self, seed: int):
        self.seed = int(seed) % 2147483647
        if self.seed <= 0:
            self.seed += 2147483646

    def next_float(self) -> float:
        self.seed = (self.seed * 16807) % 2147483647
        return (self.seed - 1) / 2147483646.0

    def next_int(self, min_val: int, max_val: int) -> int:
        return math.floor(min_val + self.next_float() * (max_val - min_val + 1))

    def nextInt(self, min_val: int, max_val: int) -> int:
        return self.next_int(min_val, max_val)


class AntiCheatEngine:
    """
    Deterministic anti-cheat validation engine for Nokia Snake.
    Simulates the entire game from the inputs to verify the integrity of the score,
    food pickups, collision points, and play duration.
    """

    @classmethod
    def validate_session(cls, session_seed: int, mode: str, difficulty: str,
                         reported_score: int, apples_eaten: int, max_length: int,
                         duration_sec: float, moves_data: list, map_walls: list = None) -> dict:
        """
        Validates gameplay and returns validation report:
        {
            'is_valid': bool,
            'verified_score': int,
            'verified_apples': int,
            'verified_length': int,
            'reason': str,
            'anomaly_type': str
        }
        """
        if map_walls is None:
            map_walls = []

        grid_w = 28
        grid_h = 16

        # Check basic bounds and structure
        if reported_score < 0 or apples_eaten < 0:
            return {
                'is_valid': False,
                'verified_score': 0,
                'verified_apples': 0,
                'verified_length': 3,
                'reason': "Negative score or apples reported",
                'anomaly_type': 'negative_values'
            }

        # Check for empty moves on high scores
        if not moves_data and reported_score > 50:
            return {
                'is_valid': False,
                'verified_score': 0,
                'verified_apples': 0,
                'verified_length': 3,
                'reason': "Missing move replay telemetry for high score",
                'anomaly_type': 'missing_telemetry'
            }

        # Max theoretical score calculation
        # In a 28x16 grid (448 tiles), max apples is 445.
        if apples_eaten > 448:
            return {
                'is_valid': False,
                'verified_score': 0,
                'verified_apples': 0,
                'verified_length': 3,
                'reason': "Apples eaten exceeds maximum possible grid capacity",
                'anomaly_type': 'grid_overflow'
            }

        # Simulation Setup
        rng = DeterministicRNG(session_seed)
        snake = [[14, 8], [13, 8], [12, 8]]  # initial 3 segments
        direction = 'R'
        score = 0
        apples = 0
        max_len = 3
        
        # Base points per difficulty
        diff_multipliers = {
            'slug': 10,
            'normal': 15,
            'python': 25,
            'cobra': 40
        }
        pts_per_apple = diff_multipliers.get(difficulty, 15)

        # Helper to generate food
        def spawn_food():
            wall_set = set(tuple(w) for w in map_walls)
            snake_set = set(tuple(s) for s in snake)
            occupied = wall_set.union(snake_set)
            
            for _ in range(500):
                fx = rng.next_int(0, grid_w - 1)
                fy = rng.next_int(0, grid_h - 1)
                if (fx, fy) not in occupied:
                    return [fx, fy]
            return None

        food = spawn_food()
        wall_set = set(tuple(w) for w in map_walls)

        # Group moves by tick index
        move_dict = {}
        for m in moves_data:
            if isinstance(m, dict) and 't' in m and 'd' in m:
                move_dict[int(m['t'])] = m['d']

        max_tick = max([int(m.get('t', 0)) for m in moves_data]) if moves_data else int(duration_sec * 10)
        max_tick = min(max_tick + 5, 20000)  # limit simulation limit

        opposites = {'U': 'D', 'D': 'U', 'L': 'R', 'R': 'L'}
        dir_offsets = {'U': [0, -1], 'D': [0, 1], 'L': [-1, 0], 'R': [1, 0]}

        game_over = False
        tick = 0

        while tick <= max_tick and not game_over:
            # Check for move in this tick
            if tick in move_dict:
                requested_dir = move_dict[tick]
                if requested_dir in ['U', 'D', 'L', 'R']:
                    if requested_dir != opposites.get(direction):
                        direction = requested_dir

            # Advance snake head
            offset = dir_offsets[direction]
            head = snake[0]
            nx = head[0] + offset[0]
            ny = head[1] + offset[1]

            # Wall collision handling depending on mode
            if mode in ['endless']:
                nx = (nx + grid_w) % grid_w
                ny = (ny + grid_h) % grid_h
            else:
                if nx < 0 or nx >= grid_w or ny < 0 or ny >= grid_h:
                    game_over = True
                    break

            # Map obstacles collision
            if (nx, ny) in wall_set:
                game_over = True
                break

            # Self collision
            if [nx, ny] in snake[:-1]:
                game_over = True
                break

            new_head = [nx, ny]
            snake.insert(0, new_head)

            # Food collision
            if food and nx == food[0] and ny == food[1]:
                apples += 1
                score += pts_per_apple
                if len(snake) > max_len:
                    max_len = len(snake)
                food = spawn_food()
                if food is None:
                    # Won game!
                    game_over = True
                    break
            else:
                snake.pop()

            tick += 1

        # Compare simulated metrics with reported metrics
        # Allow small tolerance for network latency on final tick
        score_diff = abs(reported_score - score)
        apple_diff = abs(apples_eaten - apples)

        if score_diff > (pts_per_apple * 2) or apple_diff > 2:
            return {
                'is_valid': False,
                'verified_score': score,
                'verified_apples': apples,
                'verified_length': max_len,
                'reason': f"Score mismatch: reported {reported_score} pts ({apples_eaten} apples), verified {score} pts ({apples} apples)",
                'anomaly_type': 'score_mismatch'
            }

        return {
            'is_valid': True,
            'verified_score': score,
            'verified_apples': apples,
            'verified_length': max_len,
            'reason': "Replay trace verified successfully",
            'anomaly_type': 'none'
        }
