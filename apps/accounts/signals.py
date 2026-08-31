from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import PlayerProfile

@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    if created:
        PlayerProfile.objects.create(user=instance, nickname=instance.username)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()
