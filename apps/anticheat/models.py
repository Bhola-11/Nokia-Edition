from django.db import models
from apps.game.models import GameSession

class FlaggedSession(models.Model):
    session = models.OneToOneField(GameSession, on_delete=models.CASCADE, related_name='flag_report')
    reason = models.CharField(max_length=255)
    reported_score = models.IntegerField(default=0)
    calculated_score = models.IntegerField(default=0)
    move_count = models.IntegerField(default=0)
    anomaly_type = models.CharField(max_length=50, default='score_mismatch')
    metrics = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Flagged [{self.anomaly_type}]: Session {self.session.id} (Rep: {self.reported_score} vs Calc: {self.calculated_score})"
