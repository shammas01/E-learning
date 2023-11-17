import uuid
from django.db import models
from tutor.models import TutorModel
from useraccount.models import User

# Create your models here.

# Category of course.....
class CategoryModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='course/course_file/category_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# Details of course.......
class CourseDetailsModel(models.Model):
    tutor = models.ForeignKey(TutorModel,on_delete=models.CASCADE,null=True,blank=True)
    heading = models.CharField(max_length=255,unique=True)
    contents = models.TextField()
    description  = models.TextField()
    duration = models.FloatField()
    rating = models.FloatField(null=True,blank=True)
    language = models.CharField(max_length=100)
    catogory = models.ForeignKey(CategoryModel,on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return self.heading


# Content of course.......
class CourseLessonModel(models.Model):
    course_id = models.ForeignKey(CourseDetailsModel,on_delete=models.CASCADE,related_name='course_content')
    title = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(blank=True, null=True)
    document = models.FileField(upload_to='course/course_file/documents/',null=True,blank=True)
    video = models.FileField(upload_to='course/course_file/videos/',null=True,blank=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.course_id)
    

# ratings of couerce
class CourseRatingModel(models.Model):
    course = models.ForeignKey(CourseDetailsModel,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    rating = models.FloatField()
    user_review = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating for {self.course.heading} by {self.user.username}"




