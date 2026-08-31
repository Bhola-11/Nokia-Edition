from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('', views.play_view, name='play'),
    path('api/session/start/', views.api_start_session, name='api_start_session'),
    path('api/session/submit/', views.api_submit_score, name='api_submit_score'),
    path('replays/', views.replays_list_view, name='replays_list'),
    path('replays/<uuid:session_id>/', views.replay_viewer_view, name='replay_viewer'),
]
