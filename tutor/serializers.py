from rest_framework import serializers
from .models import TutorModel, SkillModel


class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorModel
        fields = ("name","profile_picture", "skills", "resume", "phone")


class TutorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorModel
        fields = ("user", "profile_picture", "resume", "phone")

    def update(self, instance, validated_data):
        instance.profile_picture = validated_data.get("profile_picture", instance.profile_picture)
        instance.name = validated_data.get('name', instance.name)
        instance.resume = validated_data.get("resume", instance.resume)

        instance.save()
        return instance
