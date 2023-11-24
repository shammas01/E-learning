from django.conf import settings
from rest_framework import serializers
from course.models import CourseDetailsModel
from tutor.models import TutorModel
from live.models import LiveClassDetailsModel
from useraccount.models import User,UserProfile



class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class UserProfileSerializer(serializers.ModelSerializer):
    user = MyUserSerializer()

    class Meta:
        model = UserProfile
        fields = ("phone", "first_name", "last_name", "address", "user")

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.address = validated_data.get("address", instance.address)

        validated_user_data = validated_data.pop("user", None)
        user = instance.user
        if validated_user_data:
            instance.user.username = validated_user_data.get(
                "username", instance.user.username
            )
            user.save()
        instance.save()
        return instance


# for searching..............
class LiveSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiveClassDetailsModel
        fields = '__all__'


class TutorSearchSerializer(serializers.ModelSerializer):
    liveclassdetailsmodel_set = LiveSearchSerializer(many=True)
    class Meta:
        model = TutorModel
        fields = '__all__'


class CourseSearchSerializer(serializers.ModelSerializer):
    tutor = TutorSearchSerializer()
    class Meta:
        model = CourseDetailsModel
        exclude = ('catogory',)


# listing All........................
class TutorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorModel
        fields = ('id','name','profile_picture','skills','phone')


class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseDetailsModel
        fields = ('id','tutor','heading','contents','description','duration','rating','language')


class LiveListSerializer(serializers.ModelSerializer):
    class Meta:
        model =  LiveClassDetailsModel
        fields = ('id','teacher','title','session_type')



#selecting serializer....................
class TutorSelectSerializer(serializers.ModelSerializer):
    coursedetailsmodel_set = CourseListSerializer(many=True)
    liveclassdetailsmodel_set = LiveListSerializer(many=True)
    class Meta: 
        model = TutorModel
        fields = ('id','name','profile_picture','skills','phone','coursedetailsmodel_set','liveclassdetailsmodel_set')



class CourseSelectSerializer(serializers.ModelSerializer):
    tutor = TutorListSerializer()
    class Meta:
        model = CourseDetailsModel
        fields = ('id','heading','contents','description','duration','rating','language','tutor')



class LiveSelectSerializer(serializers.ModelSerializer):
    teacher = TutorListSerializer()
    class Meta:
        model = LiveClassDetailsModel
        fields = ('id',
                  'title',
                  'description',
                  'day_duration',
                  'session_type',
                  'class_start_datetime',
                  'class_duration',
                  'available_slots',
                  'pricing',
                  'session_status',
                  'created_datetime',
                  'teacher',
                )