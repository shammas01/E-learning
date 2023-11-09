from rest_framework import serializers
from . models import (CourseContentModel)



class CourseContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseContentModel
        fields = ['turor','heading','contents','description','duration','language','catogory']