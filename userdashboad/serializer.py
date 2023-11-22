from rest_framework import serializers
from course.models import CourseDetailsModel
from tutor.models import TutorModel
from live.models import LiveClassDetailsModel



class LiveListSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiveClassDetailsModel
        fields = '__all__'


class TutorListserializer(serializers.ModelSerializer):
    liveclassdetailsmodel_set = LiveListSerializer(many=True)
    class Meta:
        model = TutorModel
        fields = '__all__'


class CourseListserializer(serializers.ModelSerializer):
    tutor = TutorListserializer()
    class Meta:
        model = CourseDetailsModel
        exclude = ('rating',)



class TutorSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorModel
        fields = ('name','profile_picture','skills','phone')



class CourseSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseDetailsModel
        fields = ('tutor','contents','description','duration','rating','language')