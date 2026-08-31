from django.contrib import admin
from .models import FlaggedSession

@admin.register(FlaggedSession)
class FlaggedSessionAdmin(admin.ModelAdmin):
    list_display = ('session', 'anomaly_type', 'reported_score', 'calculated_score', 'reason', 'created_at')
    list_filter = ('anomaly_type', 'created_at')
    search_fields = ('session__id', 'reason')
