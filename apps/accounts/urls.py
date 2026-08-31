from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='my_profile'),
    path('profile/<str:username>/', views.profile_view, name='user_profile'),
    path('settings/', views.settings_view, name='settings'),
    path('api/quick-settings/', views.api_update_quick_settings, name='quick_settings'),
]
