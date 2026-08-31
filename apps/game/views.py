import json
import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib import messages
from django.utils import timezone

from .models import GameSession, Score, GameMap
from .services import ensure_preset_maps, generate_session_seed
from apps.anticheat.engine import AntiCheatEngine
from apps.anticheat.models import FlaggedSession
from apps.achievements.evaluator import AchievementEvaluator
from apps.tournaments.models import Tournament, TournamentParticipant

def play_view(request):
    ensure_preset_maps()
    maps = GameMap.objects.filter(is_active=True).order_by('difficulty_rating')
    
    # Active tournament notice if available
    now = timezone.now()
    active_tournament = Tournament.objects.filter(is_active=True, end_time__gt=now).first()
    
    # User's top scores if logged in
    user_top_score = 0
    if request.user.is_authenticated:
        user_top_score = request.user.profile.high_score

    # Global top 5 for in-game ticker
    top_scores = Score.objects.select_related('player').order_by('-score')[:5]

    context = {
        'game_maps': maps,
        'active_tournament': active_tournament,
        'user_top_score': user_top_score,
        'top_scores': top_scores,
    }
    return render(request, 'game/play.html', context)


@require_POST
def api_start_session(request):
    """
    Initializes a verified game session with a deterministic seed.
    """
    try:
        data = json.loads(request.body) if request.body else {}
        mode = data.get('mode', 'classic')
        difficulty = data.get('difficulty', 'normal')
        map_name = data.get('map_name', 'standard_box')

        seed = generate_session_seed()
        client_ip = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        session = GameSession.objects.create(
            player=request.user if request.user.is_authenticated else None,
            mode=mode,
            difficulty=difficulty,
            map_name=map_name,
            seed=seed,
            client_ip=client_ip,
            user_agent=user_agent
        )

        # Fetch map walls if challenge mode
        walls = []
        portals = []
        if mode == 'challenge':
            try:
                gmap = GameMap.objects.get(map_id=map_name)
                walls = gmap.walls_data
                portals = gmap.portals_data
            except GameMap.DoesNotExist:
                pass

        return JsonResponse({
            'status': 'success',
            'session_id': str(session.id),
            'seed': seed,
            'walls': walls,
            'portals': portals
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@require_POST
def api_submit_score(request):
    """
    Validates gameplay with the AntiCheatEngine, saves verified scores,
    evaluates achievements, and updates tournaments.
    """
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        session = get_object_or_404(GameSession, id=session_id)

        reported_score = int(data.get('score', 0))
        apples_eaten = int(data.get('apples_eaten', 0))
        max_length = int(data.get('max_length', 3))
        duration_sec = float(data.get('duration_seconds', 0.0))
        death_reason = data.get('death_reason', 'wall')
        moves_data = data.get('moves_data', [])
        checksum = data.get('checksum', '')

        # Fetch map walls for obstacle verification
        walls = []
        if session.mode == 'challenge':
            try:
                gmap = GameMap.objects.get(map_id=session.map_name)
                walls = gmap.walls_data
            except GameMap.DoesNotExist:
                pass

        # Run deterministic Anti-Cheat verification
        report = AntiCheatEngine.validate_session(
            session_seed=session.seed,
            mode=session.mode,
            difficulty=session.difficulty,
            reported_score=reported_score,
            apples_eaten=apples_eaten,
            max_length=max_length,
            duration_sec=duration_sec,
            moves_data=moves_data,
            map_walls=walls
        )

        session.score = reported_score
        session.apples_eaten = apples_eaten
        session.max_length = max_length
        session.duration_seconds = duration_sec
        session.death_reason = death_reason
        session.move_count = len(moves_data)
        session.moves_data = moves_data
        session.checksum = checksum

        if not report['is_valid']:
            session.is_flagged = True
            session.flag_reason = report['reason']
            session.save()

            FlaggedSession.objects.create(
                session=session,
                reason=report['reason'],
                reported_score=reported_score,
                calculated_score=report['verified_score'],
                move_count=len(moves_data),
                anomaly_type=report['anomaly_type'],
                metrics={'duration': duration_sec, 'apples': apples_eaten}
            )

            return JsonResponse({
                'status': 'flagged',
                'reason': report['reason'],
                'verified_score': report['verified_score']
            })

        # Session is valid!
        session.is_verified = True
        session.save()

        earned_xp = 0
        new_high_score = False
        unlocked_achievements_data = []

        if request.user.is_authenticated:
            # Create permanent Score record
            Score.objects.create(
                player=request.user,
                session=session,
                mode=session.mode,
                difficulty=session.difficulty,
                score=reported_score,
                apples_eaten=apples_eaten,
                max_length=max_length,
                duration_seconds=duration_sec
            )

            # Update player profile stats
            profile = request.user.profile
            if reported_score > profile.high_score:
                new_high_score = True

            earned_xp = profile.add_game_stats(
                score=reported_score,
                apples=apples_eaten,
                length=max_length,
                duration_sec=int(duration_sec)
            )

            # Evaluate achievements
            unlocked = AchievementEvaluator.evaluate_game(request.user, session, profile)
            unlocked_achievements_data = [
                {
                    'title': a.title,
                    'icon': a.icon,
                    'description': a.description,
                    'xp': a.xp_reward
                }
                for a in unlocked
            ]

            # Update active tournament if applicable
            now = timezone.now()
            active_tourneys = Tournament.objects.filter(
                is_active=True,
                mode=session.mode,
                difficulty=session.difficulty,
                end_time__gt=now
            )
            for tourney in active_tourneys:
                tp, _ = TournamentParticipant.objects.get_or_create(tournament=tourney, player=request.user)
                tp.attempts_count += 1
                if reported_score > tp.best_score:
                    tp.best_score = reported_score
                    tp.best_session = session
                tp.save()

        return JsonResponse({
            'status': 'verified',
            'score': reported_score,
            'apples_eaten': apples_eaten,
            'new_high_score': new_high_score,
            'earned_xp': earned_xp,
            'rank_level': request.user.profile.rank_level if request.user.is_authenticated else 1,
            'rank_title': request.user.profile.rank_title if request.user.is_authenticated else 'Guest Slider',
            'unlocked_achievements': unlocked_achievements_data
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


def replays_list_view(request):
    """Lists verified game sessions with available move data for replay."""
    replays = GameSession.objects.filter(is_verified=True).select_related('player').order_by('-score')[:30]
    return render(request, 'game/replays.html', {'replays': replays})


def replay_viewer_view(request, session_id):
    """Interactive visual replay viewer page."""
    session = get_object_or_404(GameSession, id=session_id)
    
    # Load map configuration if needed
    walls = []
    portals = []
    if session.mode == 'challenge':
        try:
            gmap = GameMap.objects.get(map_id=session.map_name)
            walls = gmap.walls_data
            portals = gmap.portals_data
        except GameMap.DoesNotExist:
            pass

    context = {
        'session': session,
        'session_json': json.dumps({
            'id': str(session.id),
            'seed': session.seed,
            'mode': session.mode,
            'difficulty': session.difficulty,
            'map_name': session.map_name,
            'score': session.score,
            'apples': session.apples_eaten,
            'duration': session.duration_seconds,
            'moves': session.moves_data,
            'walls': walls,
            'portals': portals,
            'player': session.player.username if session.player else 'Guest'
        })
    }
    return render(request, 'game/replay_viewer.html', context)
