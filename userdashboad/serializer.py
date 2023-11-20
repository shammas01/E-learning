from rest_framework import serializers
from course.models import CourseDetailsModel
from tutor.models import TutorModel


class TutorListserializer(serializers.ModelSerializer):
    class Meta:
        model = TutorModel
        fields = '__all__'


class CourseListserializer(serializers.ModelSerializer):
    tutor = TutorListserializer()
    class Meta:
        model = CourseDetailsModel
        exclude = ('rating')