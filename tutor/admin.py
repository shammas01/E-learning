from django.contrib import admin
from . models import SkillModel,TutorModel
# Register your models here.

admin.site.register(TutorModel)
admin.site.register(SkillModel)