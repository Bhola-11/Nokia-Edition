from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from apps.game.models import GameSession

class Tournament(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    emoji = models.CharField(max_length=20, default='🏆')
    mode = models.CharField(max_length=20, choices=GameSession.MODE_CHOICES, default='classic')
    difficulty = models.CharField(max_length=20, choices=GameSession.DIFFICULTY_CHOICES, default='normal')
    
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    prize_title = models.CharField(max_length=100, default='Gold 3310 Champion Trophy')
    prize_xp = models.IntegerField(default=1000)

    class Meta:
        ordering = ['-is_active', 'end_time']

    def __str__(self):
        return f"{self.emoji} {self.title} ({self.status})"

    @property
    def status(self):
        now = timezone.now()
        if now < self.start_time:
            return 'Upcoming'
        elif now > self.end_time or not self.is_active:
            return 'Ended'
        return 'Active'


class TournamentParticipant(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='participants')
    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tournament_entries')
    best_score = models.IntegerField(default=0)
    best_session = models.ForeignKey(GameSession, on_delete=models.SET_NULL, null=True, blank=True)
    attempts_count = models.IntegerField(default=0)
    last_played_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('tournament', 'player')
        ordering = ['-best_score', 'last_played_at']

    def __str__(self):
        return f"{self.player.username} in {self.tournament.title}: {self.best_score} pts"
