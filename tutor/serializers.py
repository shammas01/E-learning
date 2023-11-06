from rest_framework import serializers
from . models import TutorModel,SkillModel


class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorModel
        fields = ('user','profile_picture','skills','resume','phone')