import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from apps.game.models import GameSession, Score, GameMap
from apps.game.services import ensure_preset_maps
from apps.achievements.evaluator import ensure_default_achievements
from apps.leaderboard.models import Season
from apps.tournaments.models import Tournament, TournamentParticipant
from apps.accounts.models import PlayerProfile

class Command(BaseCommand):
    help = "Seeds database with default maps, achievements, sample users, tournaments, and verified scores."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding Nokia Snake database..."))

        # 1. Preset maps & default achievements
        ensure_preset_maps()
        ensure_default_achievements()
        self.stdout.write(self.style.SUCCESS("[OK] Preset maps and achievements initialized."))

        # 2. Season 1
        now = timezone.now()
        Season.objects.get_or_create(
            slug='season-1-genesis',
            defaults={
                'name': 'Season 1: 1999 Genesis',
                'description': 'The inaugural retro Nokia 3310 championship season.',
                'start_date': now - timedelta(days=10),
                'end_date': now + timedelta(days=50),
                'is_active': True,
                'badge_title': 'Nokia 1999 Pioneer'
            }
        )
        self.stdout.write(self.style.SUCCESS("[OK] Active Season initialized."))

        # 3. Active Tournament
        tourney, _ = Tournament.objects.get_or_create(
            slug='cobra-speed-clash',
            defaults={
                'title': 'Cobra Speed Clash 2026',
                'emoji': '⚡',
                'description': 'High speed snake tournament. Only the fastest reflexes will survive!',
                'mode': 'classic',
                'difficulty': 'cobra',
                'start_time': now - timedelta(days=2),
                'end_time': now + timedelta(days=12),
                'is_active': True,
                'prize_title': 'Crown of the Cobra King',
                'prize_xp': 2000
            }
        )
        self.stdout.write(self.style.SUCCESS("[OK] Active Tournament initialized."))

        # 4. Sample Players & Scores
        sample_users_data = [
            ('NokiaMaster_99', 'green_legend', 'classic_green', 'classic_navy', 1580, 24, 2500),
            ('PixelSerpent', 'Retro snake fan from Finland', 'amber_lcd', 'retro_silver', 1120, 18, 1800),
            ('CyberViper', 'Speedrunner and maze conqueror', 'cyan_matrix', 'cyber_yellow', 890, 14, 1400),
            ('OldSchoolGamer', '3310 unbreakable legend', 'gameboy_olive', 'ruby_red', 650, 9, 900),
            ('ByteSlider', 'Just sliding through the grid', 'dark_oled', 'stealth_black', 420, 6, 600),
        ]

        for username, bio, theme, shell, high, lvl, xp in sample_users_data:
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password('nokia1234')
                user.save()
            
            profile = user.profile
            profile.bio = bio
            profile.theme = theme
            profile.phone_shell = shell
            profile.high_score = high
            profile.rank_level = lvl
            profile.xp = xp
            profile.total_games_played = random.randint(15, 60)
            profile.total_apples_eaten = random.randint(80, 400)
            profile.max_snake_length = random.randint(15, 45)
            profile.save()

            # Create a verified session and score
            session, s_created = GameSession.objects.get_or_create(
                player=user,
                score=high,
                defaults={
                    'mode': 'classic',
                    'difficulty': 'normal',
                    'seed': random.randint(10000000, 99999999),
                    'apples_eaten': int(high / 15),
                    'max_length': min(int(high / 15) + 3, 40),
                    'duration_seconds': random.randint(45, 180),
                    'is_verified': True,
                    'death_reason': 'wall'
                }
            )

            Score.objects.get_or_create(
                player=user,
                session=session,
                defaults={
                    'mode': session.mode,
                    'difficulty': session.difficulty,
                    'score': session.score,
                    'apples_eaten': session.apples_eaten,
                    'max_length': session.max_length,
                    'duration_seconds': session.duration_seconds,
                }
            )

            # Add to tournament
            TournamentParticipant.objects.get_or_create(
                tournament=tourney,
                player=user,
                defaults={
                    'best_score': high - random.randint(0, 200),
                    'best_session': session,
                    'attempts_count': random.randint(1, 8)
                }
            )

        self.stdout.write(self.style.SUCCESS("[OK] Seeded sample players, profiles, high scores, and tournament entries."))
        self.stdout.write(self.style.SUCCESS("[SUCCESS] Nokia Snake database successfully seeded!"))
