from django.dispatch import receiver
from django.db.models.signals import post_save
from useraccount.models import User,UserProfile

@receiver(post_save,sender=User)
def create_user_profile_for_registerd_user(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)