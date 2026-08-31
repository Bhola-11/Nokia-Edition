from django.contrib import admin
from .models import Achievement, PlayerAchievement

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('icon', 'title', 'category', 'xp_reward', 'order')
    list_filter = ('category',)
    search_fields = ('title', 'description')

@admin.register(PlayerAchievement)
class PlayerAchievementAdmin(admin.ModelAdmin):
    list_display = ('player', 'achievement', 'unlocked_at')
    list_filter = ('achievement__category', 'unlocked_at')
    search_fields = ('player__username', 'achievement__title')
