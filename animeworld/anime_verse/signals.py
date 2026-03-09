import random
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, DefaultProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile.objects.create(user=instance)

        defaults = DefaultProfile.objects.filter(is_active=True, is_delete=False)

        if defaults.exists():
            profile.img_src = random.choice(list(defaults)).img_src
            profile.save()