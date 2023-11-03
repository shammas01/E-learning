from django.db import models
from useraccount.models import User
# Create your models here.

class TutorModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='tutor_files/profile/', null=True, blank=True)
    approved = models.BooleanField(default=False)
    skills = models.ManyToManyField('Skill', related_name='tutors')
    resume = models.FileField(upload_to='tutor_files/resume/', null=True, blank=True)

    def __str__(self):
        return self.user.username


class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

