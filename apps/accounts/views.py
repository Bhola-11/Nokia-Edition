from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

from .forms import UserRegistrationForm, ProfileUpdateForm
from .models import PlayerProfile
from apps.game.models import Score, GameSession

def register_view(request):
    if request.user.is_authenticated:
        return redirect('game:play')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, f"Welcome to Nokia Snake 3310, {user.username}! Ready to slide?")
            return redirect('game:play')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('game:play')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect(request.GET.get('next') or 'game:play')
        else:
            messages.error(request, "Invalid gamer tag or PIN/password.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out. Your high scores are safely stored in Nokia ROM.")
    return redirect('game:play')

def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(PlayerProfile, user__username=username)
    elif request.user.is_authenticated:
        profile = request.user.profile
    else:
        return redirect('accounts:login')
    
    recent_games = Score.objects.filter(player=profile.user).select_related('session').order_by('-created_at')[:10]
    high_scores_by_mode = {
        'classic': Score.objects.filter(player=profile.user, mode='classic').order_by('-score').first(),
        'time_attack': Score.objects.filter(player=profile.user, mode='time_attack').order_by('-score').first(),
        'endless': Score.objects.filter(player=profile.user, mode='endless').order_by('-score').first(),
        'challenge': Score.objects.filter(player=profile.user, mode='challenge').order_by('-score').first(),
    }
    
    # Achievements
    user_achievements = profile.user.unlocked_achievements.select_related('achievement').order_by('-unlocked_at')

    context = {
        'profile': profile,
        'recent_games': recent_games,
        'high_scores_by_mode': high_scores_by_mode,
        'user_achievements': user_achievements,
        'is_owner': request.user.is_authenticated and request.user == profile.user
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def settings_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Nokia 3310 settings updated successfully!")
            return redirect('accounts:settings')
    else:
        form = ProfileUpdateForm(instance=profile)
    
    return render(request, 'accounts/settings.html', {'form': form, 'profile': profile})

@require_POST
def api_update_quick_settings(request):
    """Allows instant theme / audio updates from the phone bezel buttons."""
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'guest_mode', 'message': 'Preferences kept in local session.'})
    
    try:
        data = json.loads(request.body)
        profile = request.user.profile
        
        if 'theme' in data and data['theme'] in dict(PlayerProfile.THEME_CHOICES):
            profile.theme = data['theme']
        if 'phone_shell' in data and data['phone_shell'] in dict(PlayerProfile.PHONE_SHELL_CHOICES):
            profile.phone_shell = data['phone_shell']
        if 'sound_enabled' in data:
            profile.sound_enabled = bool(data['sound_enabled'])
        if 'scanlines_enabled' in data:
            profile.scanlines_enabled = bool(data['scanlines_enabled'])
        
        profile.save()
        return JsonResponse({'status': 'success', 'theme': profile.theme, 'shell': profile.phone_shell})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
