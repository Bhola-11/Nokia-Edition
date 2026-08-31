import uuid
from django.db import models
from django.contrib.auth.models import User

class GameSession(models.Model):
    MODE_CHOICES = [
        ('classic', 'Classic Nokia'),
        ('time_attack', 'Time Attack (60s)'),
        ('endless', 'Endless Free-Roam'),
        ('challenge', 'Labyrinth Challenge'),
    ]

    DIFFICULTY_CHOICES = [
        ('slug', 'Slug (Slow - 140ms)'),
        ('normal', 'Normal (Standard - 100ms)'),
        ('python', 'Python (Fast - 70ms)'),
        ('cobra', 'Cobra (Insane - 45ms)'),
    ]

    DEATH_REASONS = [
        ('wall', 'Hit Wall'),
        ('self', 'Ate Self'),
        ('obstacle', 'Hit Obstacle'),
        ('timeout', 'Time Expired'),
        ('quit', 'Surrendered'),
        ('victory', 'Grid Filled (Max Score)'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    player = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='game_sessions')
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default='classic')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='normal')
    map_name = models.CharField(max_length=50, default='standard_box')
    
    # Determinism & Anti-Cheat
    seed = models.BigIntegerField(help_text="Deterministic PRNG seed for food & powerup spawning")
    client_ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    # Gameplay telemetry
    score = models.IntegerField(default=0)
    apples_eaten = models.IntegerField(default=0)
    max_length = models.IntegerField(default=3)
    duration_seconds = models.FloatField(default=0.0)
    move_count = models.IntegerField(default=0)
    death_reason = models.CharField(max_length=20, choices=DEATH_REASONS, default='wall')
    
    # Serialized moves for anti-cheat verification and visual replay playback
    # Format: [{"t": tick_number, "d": "U"|"D"|"L"|"R", "ms": timestamp}]
    moves_data = models.JSONField(default=list, blank=True)
    
    # Verification flags
    is_verified = models.BooleanField(default=False)
    is_flagged = models.BooleanField(default=False)
    flag_reason = models.CharField(max_length=255, blank=True)
    checksum = models.CharField(max_length=64, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        player_name = self.player.username if self.player else "Guest"
        return f"[{self.mode.upper()}] {player_name} - Score: {self.score} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"


class Score(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scores')
    session = models.OneToOneField(GameSession, on_delete=models.CASCADE, related_name='recorded_score')
    mode = models.CharField(max_length=20, choices=GameSession.MODE_CHOICES)
    difficulty = models.CharField(max_length=20, choices=GameSession.DIFFICULTY_CHOICES)
    score = models.IntegerField(db_index=True)
    apples_eaten = models.IntegerField(default=0)
    max_length = models.IntegerField(default=3)
    duration_seconds = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-score', 'duration_seconds']
        indexes = [
            models.Index(fields=['mode', '-score']),
            models.Index(fields=['difficulty', '-score']),
            models.Index(fields=['created_at', '-score']),
        ]

    def __str__(self):
        return f"{self.player.username} - {self.score} pts ({self.mode})"


class GameMap(models.Model):
    map_id = models.SlugField(primary_key=True, max_length=50)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    grid_width = models.IntegerField(default=28)
    grid_height = models.IntegerField(default=16)
    walls_data = models.JSONField(default=list, help_text="List of [x, y] coordinates of solid blocks")
    portals_data = models.JSONField(default=list, help_text="Pairs of [{entry: [x,y], exit: [x,y]}]")
    difficulty_rating = models.IntegerField(default=1)  # 1 to 5 stars
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.grid_width}x{self.grid_height})"
