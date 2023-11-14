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
class CourseContentModel(models.Model):
    course_id = models.ForeignKey(CourseDetailsModel,on_delete=models.CASCADE,related_name='course_content')
    title = models.CharField(max_length=255,null=True,blank=True,unique=True)
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

    VISIBILITY_CHOICES = [
        ('Public', 'Public'),
        ('Private', 'Private'),
        ('Unlisted', 'Unlisted'),
    ]

    teacher = models.ForeignKey(TutorModel, on_delete=models.CASCADE)  # Reference to the teacher (User model)
    title = models.CharField(max_length=255)  # Title of the live session
    description = models.TextField()  # Detailed description of the session
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE,blank=True,null=True)  # Reference to the subject or category
    duration = models.FloatField()
    session_type = models.CharField(max_length=12, choices=SESSION_TYPES)  # Session type
    class_start_datetime = models.DateTimeField()  # Scheduled start date and time
    class_duration = models.PositiveIntegerField(null=True,blank=True)  # Duration of the session (in minutes)
    max_slots = models.PositiveIntegerField()  # Maximum number of student slots
    available_slots = models.PositiveIntegerField()  # Number of available student slots
    pricing = models.DecimalField(max_digits=10, decimal_places=2)  # Cost of the session
    session_status = models.CharField(max_length=12, choices=SESSION_STATUSES)  # Session status
    created_datetime = models.DateTimeField(auto_now_add=True)  # Date and time of session creation
    last_updated_datetime = models.DateTimeField(auto_now=True)  # Date and time of the last updateccccccccccccccc6
    visibility = models.CharField(max_length=12, choices=VISIBILITY_CHOICES)  # Session visibility

    def __str__(self):
        return self.title
    

# Contents of live class
class LiveClassContentsModel(models.Model):
    live_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    live_session = models.ForeignKey(LiveClassDetailsModel, on_delete=models.CASCADE)
    recording_url = models.URLField(max_length=200, blank=True, null=True)
    materials_resources = models.TextField(blank=True, null=True)
    session_url = models.URLField(max_length=200, blank=True, null=True)
    cancellation_policy = models.TextField(blank=True, null=True)
    session_images = models.ImageField(upload_to='course/course_file/live_images/', blank=True, null=True)

    def __str__(self):
        return f"LiveClassContent ID: {self.live_id} for Live Session: {self.live_session.id}"