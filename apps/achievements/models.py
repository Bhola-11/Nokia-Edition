from django.db import models
from django.contrib.auth.models import User

class Achievement(models.Model):
    CATEGORY_CHOICES = [
        ('score', 'Score Milestones'),
        ('skill', 'Skill & Speed'),
        ('grind', 'Dedication & Stats'),
        ('mode', 'Game Mode Feats'),
    ]

    slug = models.SlugField(primary_key=True, max_length=50)
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=20, default='🏆')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='score')
    xp_reward = models.PositiveIntegerField(default=100)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'slug']

    def __str__(self):
        return f"{self.icon} {self.title} (+{self.xp_reward} XP)"


class PlayerAchievement(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='unlocked_achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='unlocks')
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('player', 'achievement')
        ordering = ['-unlocked_at']

    def __str__(self):
        return f"{self.player.username} unlocked {self.achievement.title}"
