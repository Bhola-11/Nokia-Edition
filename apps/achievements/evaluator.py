from .models import Achievement, PlayerAchievement

DEFAULT_ACHIEVEMENTS = [
    {
        'slug': 'first_bite',
        'title': 'First Bite',
        'description': 'Eat your first apple on the Nokia 3310 screen.',
        'icon': '🍎',
        'category': 'score',
        'xp_reward': 50,
        'order': 1
    },
    {
        'slug': 'centurion',
        'title': 'Centurion',
        'description': 'Score 100 points in a single classic match.',
        'icon': '💯',
        'category': 'score',
        'xp_reward': 100,
        'order': 2
    },
    {
        'slug': 'century_club',
        'title': 'Century Club',
        'description': 'Score 500 points in a single match.',
        'icon': '🥈',
        'category': 'score',
        'xp_reward': 250,
        'order': 3
    },
    {
        'slug': 'master_3310',
        'title': 'Master of 3310',
        'description': 'Score 1,000 points in a single match.',
        'icon': '🥇',
        'category': 'score',
        'xp_reward': 500,
        'order': 4
    },
    {
        'slug': 'ouroboros_god',
        'title': 'Ouroboros God',
        'description': 'Reach 2,500 points in one game session. Legendary status.',
        'icon': '👑',
        'category': 'score',
        'xp_reward': 1500,
        'order': 5
    },
    {
        'slug': 'long_boy',
        'title': 'Long Boy',
        'description': 'Grow snake length to 25 segments.',
        'icon': '🐍',
        'category': 'skill',
        'xp_reward': 150,
        'order': 6
    },
    {
        'slug': 'anaconda',
        'title': 'Anaconda',
        'description': 'Grow snake length to 50 segments without crashing.',
        'icon': '🐉',
        'category': 'skill',
        'xp_reward': 350,
        'order': 7
    },
    {
        'slug': 'speed_demon',
        'title': 'Speed Demon',
        'description': 'Score 300+ points on Cobra (Insane) difficulty.',
        'icon': '⚡',
        'category': 'skill',
        'xp_reward': 300,
        'order': 8
    },
    {
        'slug': 'time_attack_champ',
        'title': 'Time Attack Champ',
        'description': 'Score 300+ points in 60s Time Attack mode.',
        'icon': '⏱️',
        'category': 'mode',
        'xp_reward': 200,
        'order': 9
    },
    {
        'slug': 'labyrinth_victor',
        'title': 'Labyrinth Victor',
        'description': 'Score 300+ points in Labyrinth Challenge mode.',
        'icon': '🏰',
        'category': 'mode',
        'xp_reward': 250,
        'order': 10
    },
    {
        'slug': 'survivor',
        'title': 'Survivor',
        'description': 'Survive for more than 3 minutes in a single continuous session.',
        'icon': '🛡️',
        'category': 'skill',
        'xp_reward': 200,
        'order': 11
    },
    {
        'slug': 'snake_addict',
        'title': 'Snake Addict',
        'description': 'Play 25 total games on your Nokia.',
        'icon': '🎮',
        'category': 'grind',
        'xp_reward': 150,
        'order': 12
    },
    {
        'slug': 'apple_orchard',
        'title': 'Apple Orchard',
        'description': 'Eat 250 total apples across your career.',
        'icon': '🍏',
        'category': 'grind',
        'xp_reward': 300,
        'order': 13
    },
    {
        'slug': 'nokia_veteran',
        'title': 'Nokia Veteran',
        'description': 'Reach Player Rank Level 10.',
        'icon': '🎖️',
        'category': 'grind',
        'xp_reward': 500,
        'order': 14
    },
]

def ensure_default_achievements():
    for item in DEFAULT_ACHIEVEMENTS:
        Achievement.objects.update_or_create(
            slug=item['slug'],
            defaults={
                'title': item['title'],
                'description': item['description'],
                'icon': item['icon'],
                'category': item['category'],
                'xp_reward': item['xp_reward'],
                'order': item['order'],
            }
        )

class AchievementEvaluator:
    @classmethod
    def evaluate_game(cls, user, session, profile) -> list:
        """
        Evaluates conditions and awards any newly unlocked achievements.
        Returns list of newly unlocked Achievement objects.
        """
        if not user or not user.is_authenticated:
            return []

        ensure_default_achievements()
        unlocked_now = []
        already_unlocked = set(PlayerAchievement.objects.filter(player=user).values_list('achievement__slug', flat=True))

        checks = [
            ('first_bite', session.apples_eaten >= 1),
            ('centurion', session.score >= 100),
            ('century_club', session.score >= 500),
            ('master_3310', session.score >= 1000),
            ('ouroboros_god', session.score >= 2500),
            ('long_boy', session.max_length >= 25),
            ('anaconda', session.max_length >= 50),
            ('speed_demon', session.difficulty == 'cobra' and session.score >= 300),
            ('time_attack_champ', session.mode == 'time_attack' and session.score >= 300),
            ('labyrinth_victor', session.mode == 'challenge' and session.score >= 300),
            ('survivor', session.duration_seconds >= 180),
            ('snake_addict', profile.total_games_played >= 25),
            ('apple_orchard', profile.total_apples_eaten >= 250),
            ('nokia_veteran', profile.rank_level >= 10),
        ]

        for slug, passed in checks:
            if passed and slug not in already_unlocked:
                try:
                    ach = Achievement.objects.get(slug=slug)
                    PlayerAchievement.objects.create(player=user, achievement=ach)
                    profile.xp += ach.xp_reward
                    unlocked_now.append(ach)
                except Achievement.DoesNotExist:
                    pass

        if unlocked_now:
            profile.save()

        return unlocked_now
