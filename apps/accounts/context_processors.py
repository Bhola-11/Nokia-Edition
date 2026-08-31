def player_context(request):
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        return {
            'player_profile': request.user.profile,
            'active_theme': request.user.profile.theme,
            'active_shell': request.user.profile.phone_shell,
        }
    return {
        'player_profile': None,
        'active_theme': 'classic_green',
        'active_shell': 'classic_navy',
    }
