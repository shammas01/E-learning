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
        fields = ('tutor','heading','contents','description','duration','rating','language')



class LiveSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model =  LiveClassDetailsModel
        fields = ('teacher','title','day_duration','session_type','pricing')