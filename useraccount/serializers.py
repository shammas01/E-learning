from rest_framework import serializers
from . models import User,UserProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class Emailsmtpserializer(serializers.Serializer):
    email = serializers.EmailField()

class EmailOtpSerializer(serializers.Serializer):
    otp = serializers.IntegerField()


class MyTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user,*args):
        token = super().get_token(user)
        if user.username:
            token['username'] = user.username
        if user.email:
            token['email'] = user.email
          
        return token
    

class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email')


class UserProfileSerializer(serializers.ModelSerializer):
    user = MyUserSerializer()
    class Meta:
        model= UserProfile
        fields = ('phone','first_name','last_name','address','user')

    def update(self,instance,validated_data):
        instance.phone = validated_data.get('phone',instance.phone)
        instance.first_name = validated_data.get('first_name',instance.first_name)
        instance.last_name = validated_data.get('last_name',instance.last_name)
        instance.address = validated_data.get('address',instance.address)
        
        validated_user_data = validated_data.pop('user',None)       
        if validated_user_data:          
            instance.user.username = validated_user_data.get('username',instance.user.username)
            instance.user.email = validated_user_data.get('email',instance.user.email)
        return instance
        