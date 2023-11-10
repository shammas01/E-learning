from django.dispatch import receiver
from django.db.models.signals import post_save
from course.models import CourseDetailsModel,CourseContentModel


@receiver(post_save, sender=CourseDetailsModel)
def create_user_profile_for_registerd_user(sender, instance, created, **kwargs):
    if created:
        CourseContentModel.objects.create(course_id=instance)