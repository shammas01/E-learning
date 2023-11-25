from django.db import models
from useraccount.models import User
from course.models import CourseDetailsModel

# Create your models here.

class UserCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user.email)


class CartItem(models.Model):
    cart = models.ForeignKey(UserCart, on_delete=models.CASCADE)
    course = models.ForeignKey(CourseDetailsModel, on_delete=models.CASCADE)

    @property
    def total_cost(self):
        return  self.course.price
    
    def __str__(self):
        return str(self.course.heading)