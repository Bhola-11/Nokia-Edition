from django.contrib import admin
from .models import Season

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'start_date', 'end_date', 'is_active', 'badge_title')
    list_filter = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}
