from django.contrib import admin
from .models import GameSession, Score, GameMap

@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'player', 'mode', 'difficulty', 'score', 'apples_eaten', 'is_verified', 'is_flagged', 'created_at')
    list_filter = ('mode', 'difficulty', 'is_verified', 'is_flagged', 'created_at')
    search_fields = ('player__username', 'id', 'flag_reason')

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('player', 'score', 'mode', 'difficulty', 'apples_eaten', 'duration_seconds', 'created_at')
    list_filter = ('mode', 'difficulty', 'created_at')
    search_fields = ('player__username',)
    ordering = ('-score',)

@admin.register(GameMap)
class GameMapAdmin(admin.ModelAdmin):
    list_display = ('map_id', 'name', 'grid_width', 'grid_height', 'difficulty_rating', 'is_active')
    list_filter = ('is_active', 'difficulty_rating')
