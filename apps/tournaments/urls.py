from django.urls import path
from . import views

app_name = 'tournaments'

urlpatterns = [
    path('', views.tournament_list_view, name='list'),
    path('<slug:slug>/', views.tournament_detail_view, name='detail'),
    path('<slug:slug>/join/', views.tournament_join_view, name='join'),
]
