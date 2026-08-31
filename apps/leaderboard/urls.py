from django.urls import path
from . import views

app_name = 'leaderboard'

urlpatterns = [
    path('', views.leaderboard_view, name='index'),
    path('api/live/', views.api_live_leaderboard, name='api_live'),
]
