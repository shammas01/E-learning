from django.contrib import admin
from . models import (
            CategoryModel,
            CourseLessonModel,
            CourseDetailsModel,
            CourseRatingModel,
  
            )
# Register your models here.

admin.site.register(CategoryModel)
admin.site.register(CourseDetailsModel)
admin.site.register(CourseLessonModel)
admin.site.register(CourseRatingModel)


