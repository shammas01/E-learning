from django.db import models
from useraccount.models import User

# Create your models here.


class TutorModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to="tutor_files/profile/", null=True, blank=True
    )
    approved = models.BooleanField(default=False)
    skills = models.ManyToManyField(
        "SkillModel", related_name="tutors", null=True, blank=True
    )
    resume = models.FileField(upload_to="tutor_files/resume/", null=True, blank=True)
    phone = models.CharField(max_length=13, unique=True, null=True)
    is_block = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)


class SkillModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)
