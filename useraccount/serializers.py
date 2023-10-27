from rest_framework import serializers
from . models import User,UserProfile


class Emailsmtpserializer(serializers.Serializer):
    email = serializers.EmailField()


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email')