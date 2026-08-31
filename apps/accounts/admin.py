from django.contrib import admin
from .models import PlayerProfile

@admin.register(PlayerProfile)
class PlayerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name', 'rank_level', 'high_score', 'total_score', 'total_games_played', 'theme')
    list_filter = ('theme', 'phone_shell', 'rank_level')
    search_fields = ('user__username', 'nickname', 'bio')
    ordering = ('-high_score', '-xp')
