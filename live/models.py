from datetime import timezone
from django.db import models
import uuid
from course.models import CategoryModel
from tutor.models import TutorModel


# class CategoryModel(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField(blank=True, null=True)
#     image = models.ImageField(upload_to='course/course_file/category_images/', blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# Create your models here.



# Details of live class
class LiveClassDetailsModel(models.Model):
    SESSION_TYPES = [
        ('One-to-Many', 'One-To-Many'),
        ('One-on-One', 'One-on-One'),
        ('Group', 'Group'),
    ]

    SESSION_STATUSES = [
        ('Planned', 'Planned'),
        ('Published', 'Published'),
    ]

    
    teacher = models.ForeignKey(TutorModel, on_delete=models.CASCADE)  
    title = models.CharField(max_length=255)  
    description = models.TextField(null=True,blank=True)  
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE,blank=True,null=True)  
    day_duration = models.IntegerField()
    session_type = models.CharField(max_length=12, default='One-to-Many',choices=SESSION_TYPES,null=True)  
    class_start_datetime = models.DateTimeField()  
    class_duration = models.PositiveIntegerField(null=True,blank=True)  
    max_slots = models.PositiveIntegerField()  
    available_slots = models.PositiveIntegerField(null=True,blank=True)  
    pricing = models.PositiveIntegerField(null=True,blank=True) 
    session_status = models.CharField(max_length=12, default="Planned",choices=SESSION_STATUSES,null=True)  
    created_datetime = models.DateTimeField(auto_now_add=True)  
    last_updated_datetime = models.DateTimeField(auto_now=True)  
    

    def save(self, *args, **kwargs):
        self.last_updated_datetime = models.DateField(auto_now_add=True)
        super(LiveClassDetailsModel, self).save(*args, **kwargs)


    def __str__(self):
        return self.title
    

# Contents of live class
class LiveClassContentsModel(models.Model):
    SESSION_TYPES = [
        ('Completed', 'Completed'),
        ('On-Going', 'On-Going'),
        ('Up-Comming', 'Up-Comming'),
    ]

    live_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    live_session = models.ForeignKey(LiveClassDetailsModel, on_delete=models.CASCADE)
    recording_url = models.URLField(max_length=200, blank=True, null=True)
    materials_resources = models.TextField(blank=True, null=True)
    session_url = models.URLField(max_length=200, blank=True, null=True)
    cancellation_policy = models.TextField(blank=True, null=True)
    status=models.CharField(max_length=20,choices=SESSION_TYPES,default='Up-Comming')
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"LiveClassContent ID: {self.live_id} for Live Session: {self.live_session.id}"
    
    