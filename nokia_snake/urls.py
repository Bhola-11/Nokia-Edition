from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.game.urls', namespace='game')),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('leaderboard/', include('apps.leaderboard.urls', namespace='leaderboard')),
    path('achievements/', include('apps.achievements.urls', namespace='achievements')),
    path('tournaments/', include('apps.tournaments.urls', namespace='tournaments')),
    path('analytics/', include('apps.analytics.urls', namespace='analytics')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
