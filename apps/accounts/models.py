from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class PlayerProfile(models.Model):
    THEME_CHOICES = [
        ('classic_green', 'Nokia 3310 Classic Green LCD (#9bbc0f)'),
        ('amber_lcd', 'Vintage Amber LCD (#f39c12)'),
        ('cyan_matrix', 'Cyber Cyan Matrix (#00ffff)'),
        ('gameboy_olive', 'Retro GameBoy Olive (#8bac0f)'),
        ('dark_oled', 'Monochrome Dark OLED (#e0e0e0)'),
    ]

    PHONE_SHELL_CHOICES = [
        ('classic_navy', 'Nokia 3310 Classic Navy Blue'),
        ('retro_silver', 'Silver Metallic Edition'),
        ('ruby_red', 'Ruby Red Passion'),
        ('stealth_black', 'Stealth Charcoal Black'),
        ('cyber_yellow', 'Cyberpunk Neon Yellow'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nickname = models.CharField(max_length=50, blank=True)
    bio = models.TextField(max_length=300, blank=True)
    
    # Customization & Visuals
    theme = models.CharField(max_length=30, choices=THEME_CHOICES, default='classic_green')
    phone_shell = models.CharField(max_length=30, choices=PHONE_SHELL_CHOICES, default='classic_navy')
    sound_enabled = models.BooleanField(default=True)
    sound_volume = models.IntegerField(default=80)  # 0 to 100
    vibration_enabled = models.BooleanField(default=True)
    scanlines_enabled = models.BooleanField(default=True)
    touch_controls_enabled = models.BooleanField(default=True)

    # Statistics & Records
    total_games_played = models.PositiveIntegerField(default=0)
    high_score = models.PositiveIntegerField(default=0)
    total_score = models.BigIntegerField(default=0)
    total_apples_eaten = models.PositiveIntegerField(default=0)
    max_snake_length = models.PositiveIntegerField(default=3)
    total_playtime_seconds = models.PositiveIntegerField(default=0)
    xp = models.PositiveIntegerField(default=0)
    rank_level = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-high_score', '-xp']

    def __str__(self):
        return f"{self.display_name} (Rank {self.rank_level} | High: {self.high_score})"

    @property
    def display_name(self):
        return self.nickname or self.user.username

    def add_game_stats(self, score, apples, length, duration_sec):
        self.total_games_played += 1
        self.total_score += score
        self.total_apples_eaten += apples
        self.total_playtime_seconds += duration_sec
        if score > self.high_score:
            self.high_score = score
        if length > self.max_snake_length:
            self.max_snake_length = length
        
        # XP Calculation: base score + bonus per apple + survival time bonus
        earned_xp = int((score * 1.5) + (apples * 5) + (duration_sec * 0.5))
        self.xp += earned_xp
        
        # Level progression formula: Level = sqrt(xp / 100) + 1
        self.rank_level = int((self.xp / 100) ** 0.5) + 1
        self.save()
        return earned_xp

    @property
    def rank_title(self):
        titles = [
            (1, "Worm Cadet"),
            (5, "Garden Snake"),
            (10, "Copperhead"),
            (15, "Viper Scout"),
            (25, "Rattlesnake Pro"),
            (40, "Python Master"),
            (60, "Black Mamba"),
            (80, "King Cobra"),
            (100, "Nokia Ouroboros Legend"),
        ]
        for lvl, title in reversed(titles):
            if self.rank_level >= lvl:
                return title
        return "Worm Cadet"
