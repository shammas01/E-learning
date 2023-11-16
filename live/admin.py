from django.contrib import admin
from . models import LiveClassDetailsModel,LiveClassContentsModel
# Register your models here.

admin.site.register(LiveClassDetailsModel)
admin.site.register(LiveClassContentsModel)