from rest_framework import serializers
from . models import User


class Emailsmtpserializer(serializers.Serializer):
    email = serializers.CharField()
    