from django.db import models
from django.utils import timezone

class Season(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    badge_title = models.CharField(max_length=50, default="Season 1 Contender")

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.name} ({'Active' if self.is_active else 'Closed'})"
