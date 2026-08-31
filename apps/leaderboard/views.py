from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from apps.game.models import Score
from apps.accounts.models import PlayerProfile

def leaderboard_view(request):
    mode_filter = request.GET.get('mode', 'all')
    diff_filter = request.GET.get('difficulty', 'all')
    time_filter = request.GET.get('time', 'all_time')

    scores_qs = Score.objects.select_related('player', 'player__profile', 'session').order_by('-score', 'duration_seconds')

    if mode_filter != 'all':
        scores_qs = scores_qs.filter(mode=mode_filter)

    if diff_filter != 'all':
        scores_qs = scores_qs.filter(difficulty=diff_filter)

    now = timezone.now()
    if time_filter == 'today':
        scores_qs = scores_qs.filter(created_at__gte=now - timedelta(days=1))
    elif time_filter == 'weekly':
        scores_qs = scores_qs.filter(created_at__gte=now - timedelta(days=7))
    elif time_filter == 'monthly':
        scores_qs = scores_qs.filter(created_at__gte=now - timedelta(days=30))

    top_scores = scores_qs[:100]

    # Calculate rank numbers and highest tier badges
    ranked_scores = []
    for i, s in enumerate(top_scores, start=1):
        ranked_scores.append({
            'rank': i,
            'score': s,
        })

    # Top overall players by XP
    top_xp_players = PlayerProfile.objects.select_related('user').order_by('-xp')[:10]

    context = {
        'ranked_scores': ranked_scores,
        'top_xp_players': top_xp_players,
        'current_mode': mode_filter,
        'current_difficulty': diff_filter,
        'current_time': time_filter,
        'total_entries': scores_qs.count(),
    }
    return render(request, 'leaderboard/leaderboard.html', context)


def api_live_leaderboard(request):
    """API endpoint for in-game real-time high score ticker."""
    mode = request.GET.get('mode', 'classic')
    scores = Score.objects.filter(mode=mode).select_related('player').order_by('-score')[:10]
    
    data = [
        {
            'rank': idx + 1,
            'player': s.player.username,
            'score': s.score,
            'difficulty': s.difficulty,
            'date': s.created_at.strftime('%b %d')
        }
        for idx, s in enumerate(scores)
    ]
    return JsonResponse({'status': 'success', 'mode': mode, 'leaderboard': data})
