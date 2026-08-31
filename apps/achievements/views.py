from django.shortcuts import render
from .models import Achievement, PlayerAchievement
from .evaluator import ensure_default_achievements

def achievements_list_view(request):
    ensure_default_achievements()
    achievements = Achievement.objects.all().order_by('order')
    
    unlocked_slugs = set()
    if request.user.is_authenticated:
        unlocked_slugs = set(
            PlayerAchievement.objects.filter(player=request.user)
            .values_list('achievement__slug', flat=True)
        )

    categories = {
        'score': 'Score Milestones',
        'skill': 'Skill & Speed',
        'mode': 'Game Mode Feats',
        'grind': 'Dedication & Career',
    }

    categorized = {}
    for cat_key, cat_title in categories.items():
        categorized[cat_title] = [
            {
                'obj': a,
                'is_unlocked': a.slug in unlocked_slugs
            }
            for a in achievements if a.category == cat_key
        ]

    unlocked_count = len(unlocked_slugs)
    total_count = achievements.count()
    progress_percent = int((unlocked_count / total_count * 100)) if total_count else 0

    context = {
        'categorized_achievements': categorized,
        'unlocked_count': unlocked_count,
        'total_count': total_count,
        'progress_percent': progress_percent,
    }
    return render(request, 'achievements/list.html', context)
