from django.dispatch import receiver
from django.db.models.signals import post_save
from useraccount.models import User, UserProfile
from userdashboad.models import UserCart


@receiver(post_save, sender=User)
def create_user_profile_for_registerd_user(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        UserCart.objects.create(user=instance)