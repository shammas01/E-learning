from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from . models import LiveClassDetailsModel


@receiver(pre_save, sender=LiveClassDetailsModel)
def update_last_updated_datetime(sender, instance, **kwargs):
    instance.last_updated_datetime = timezone.now()