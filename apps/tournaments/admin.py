from django.contrib import admin
from .models import Tournament, TournamentParticipant

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('title', 'mode', 'difficulty', 'start_time', 'end_time', 'is_active', 'prize_title')
    list_filter = ('mode', 'difficulty', 'is_active')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(TournamentParticipant)
class TournamentParticipantAdmin(admin.ModelAdmin):
    list_display = ('tournament', 'player', 'best_score', 'attempts_count', 'last_played_at')
    list_filter = ('tournament',)
    search_fields = ('player__username',)
