import random
import time
from .models import GameMap

PRESET_MAPS = [
    {
        'map_id': 'standard_box',
        'name': 'Classic 3310 Box',
        'description': 'The authentic 1999 Nokia snake arena with outer border boundary.',
        'grid_width': 28,
        'grid_height': 16,
        'walls_data': [],
        'portals_data': [],
        'difficulty_rating': 1,
    },
    {
        'map_id': 'cross_labyrinth',
        'name': 'Cross Labyrinth',
        'description': 'Four quadrant arena divided by central cross barricades with tight pass-throughs.',
        'grid_width': 28,
        'grid_height': 16,
        'walls_data': [
            # Vertical central pillars leaving middle and edge gaps
            [14, 2], [14, 3], [14, 4], [14, 5],
            [14, 10], [14, 11], [14, 12], [14, 13],
            # Horizontal cross beams
            [5, 8], [6, 8], [7, 8], [8, 8], [9, 8],
            [18, 8], [19, 8], [20, 8], [21, 8], [22, 8],
        ],
        'portals_data': [],
        'difficulty_rating': 2,
    },
    {
        'map_id': 'four_rooms',
        'name': 'Four Chambers',
        'description': 'Four interconnected rooms with narrow doors. Extreme claustrophobia as snake grows.',
        'grid_width': 28,
        'grid_height': 16,
        'walls_data': [
            # Vertical divider with 2 doors
            [14, 0], [14, 1], [14, 2], [14, 3], [14, 4], [14, 5],
            [14, 9], [14, 10], [14, 11], [14, 12], [14, 13], [14, 14], [14, 15],
            # Horizontal divider with 2 doors
            [0, 8], [1, 8], [2, 8], [3, 8], [4, 8], [5, 8],
            [9, 8], [10, 8], [11, 8], [12, 8], [13, 8],
            [15, 8], [16, 8], [17, 8], [18, 8],
            [22, 8], [23, 8], [24, 8], [25, 8], [26, 8], [27, 8]
        ],
        'portals_data': [],
        'difficulty_rating': 3,
    },
    {
        'map_id': 'twin_portals',
        'name': 'Quantum Warp Pipes',
        'description': 'Teleport instantly across opposite corners through mystic Nokia quantum portals!',
        'grid_width': 28,
        'grid_height': 16,
        'walls_data': [
            [6, 4], [6, 5], [6, 6], [6, 9], [6, 10], [6, 11],
            [21, 4], [21, 5], [21, 6], [21, 9], [21, 10], [21, 11]
        ],
        'portals_data': [
            {'entry': [2, 2], 'exit': [25, 13], 'color': '#00ffff'},
            {'entry': [2, 13], 'exit': [25, 2], 'color': '#ff00ff'},
        ],
        'difficulty_rating': 4,
    },
    {
        'map_id': 'serpentine_circuit',
        'name': 'Circuit Board',
        'description': 'High speed circuit tracks designed for master navigators.',
        'grid_width': 28,
        'grid_height': 16,
        'walls_data': [
            [4, 3], [5, 3], [6, 3], [7, 3], [8, 3], [9, 3], [10, 3],
            [17, 3], [18, 3], [19, 3], [20, 3], [21, 3], [22, 3], [23, 3],
            [4, 12], [5, 12], [6, 12], [7, 12], [8, 12], [9, 12], [10, 12],
            [17, 12], [18, 12], [19, 12], [20, 12], [21, 12], [22, 12], [23, 12],
            [13, 6], [14, 6], [13, 9], [14, 9]
        ],
        'portals_data': [],
        'difficulty_rating': 5,
    }
]

def ensure_preset_maps():
    for item in PRESET_MAPS:
        GameMap.objects.update_or_create(
            map_id=item['map_id'],
            defaults={
                'name': item['name'],
                'description': item['description'],
                'grid_width': item['grid_width'],
                'grid_height': item['grid_height'],
                'walls_data': item['walls_data'],
                'portals_data': item['portals_data'],
                'difficulty_rating': item['difficulty_rating'],
                'is_active': True,
            }
        )

def generate_session_seed():
    """Generates an integer seed using time and randomness."""
    return random.randint(10000000, 99999999)
