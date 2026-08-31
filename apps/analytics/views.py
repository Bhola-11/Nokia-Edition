from django.shortcuts import render
from django.db.models import Avg, Sum, Count, Max
from apps.game.models import GameSession, Score
from apps.accounts.models import PlayerProfile
from apps.anticheat.models import FlaggedSession

def analytics_dashboard_view(request):
    total_sessions = GameSession.objects.count()
    total_players = PlayerProfile.objects.count()
    total_apples = GameSession.objects.aggregate(total=Sum('apples_eaten'))['total'] or 0
    all_time_high = Score.objects.aggregate(high=Max('score'))['high'] or 0
    avg_score = Score.objects.aggregate(avg=Avg('score'))['avg'] or 0

    # Mode distribution
    mode_counts = list(GameSession.objects.values('mode').annotate(count=Count('id')).order_by('-count'))
    # Difficulty distribution
    difficulty_counts = list(GameSession.objects.values('difficulty').annotate(count=Count('id')).order_by('-count'))
    # Death cause analysis
    death_causes = list(GameSession.objects.values('death_reason').annotate(count=Count('id')).order_by('-count'))
    
    # Anti-cheat flags
    flagged_sessions = FlaggedSession.objects.select_related('session').order_by('-created_at')[:15]
    total_flagged = FlaggedSession.objects.count()

    context = {
        'total_sessions': total_sessions,
        'total_players': total_players,
        'total_apples': total_apples,
        'all_time_high': all_time_high,
        'avg_score': round(avg_score, 1),
        'mode_counts': mode_counts,
        'difficulty_counts': difficulty_counts,
        'death_causes': death_causes,
        'flagged_sessions': flagged_sessions,
        'total_flagged': total_flagged,
    }
    return render(request, 'analytics/dashboard.html', context)
