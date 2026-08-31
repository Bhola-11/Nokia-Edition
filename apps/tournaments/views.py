from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Tournament, TournamentParticipant

def tournament_list_view(request):
    now = timezone.now()
    active_tournaments = Tournament.objects.filter(is_active=True, end_time__gt=now).order_by('end_time')
    past_tournaments = Tournament.objects.filter(models_q_or_ended=True) if False else Tournament.objects.filter(end_time__lte=now).order_by('-end_time')[:10]

    context = {
        'active_tournaments': active_tournaments,
        'past_tournaments': past_tournaments,
    }
    return render(request, 'tournaments/list.html', context)

def tournament_detail_view(request, slug):
    tournament = get_object_or_404(Tournament, slug=slug)
    participants = tournament.participants.select_related('player', 'player__profile').order_by('-best_score')
    
    user_entry = None
    if request.user.is_authenticated:
        user_entry = participants.filter(player=request.user).first()

    context = {
        'tournament': tournament,
        'participants': participants,
        'user_entry': user_entry,
    }
    return render(request, 'tournaments/detail.html', context)

@login_required
def tournament_join_view(request, slug):
    tournament = get_object_or_404(Tournament, slug=slug)
    TournamentParticipant.objects.get_or_create(tournament=tournament, player=request.user)
    messages.success(request, f"Joined tournament '{tournament.title}'! Good luck!")
    return redirect('tournaments:detail', slug=slug)
