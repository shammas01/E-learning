from rest_framework import serializers

from useraccount import google
from useraccount.register import register_social_user
from . models import User,UserProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

class Emailsmtpserializer(serializers.Serializer):
    email = serializers.EmailField()

class OtpSerializer(serializers.Serializer):
    otp = serializers.IntegerField()

class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

class PhoneOtpSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

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
        instance.save()
        return instance



    
    
    def validate_auth_token(self,auth_token):
        user_data = google.Google.validate(auth_token)
        print('user data= ',user_data)
        try:
            user_data['sub']
            print("user data sub=",user_data['sub'])
        except:
            raise serializers.ValidationError(
                'The token is expired or invalid. Please login again.'
            )
        if user_data['aud'] != settings.GOOGLE_CLIENT_ID:
            raise AuthenticationFailed('oops, who are you?')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        
        return register_social_user(
            user_id=user_id,email=email,name=name,
        )




# google retuned data from when we pass auth token.    
user_data=  {
            'iss': 'https://accounts.google.com',
            'azp': '222479872742-1vqubtpstg8oitu34qb9hmb0f49q9bde.apps.googleusercontent.com',
            'aud': '222479872742-1vqubtpstg8oitu34qb9hmb0f49q9bde.apps.googleusercontent.com',
            'sub': '113454620181132250584',
            'email': 'shammasvavad@gmail.com',
            'email_verified': True,
            'at_hash': '8LAwpF45JSXjZpTghbxpHQ',
            'name': 'Shammas Tk',
            'picture': 'https://lh3.googleusercontent.com/a/ACg8ocKr7GFFoMyXbqqiEJ7qNtVUruMTLCsIl9oiHvu8QbdvKA=s96-c',
            'given_name': 'Shammas',
            'family_name': 'Tk',
            'locale': 'en-GB',
            'iat': 1698670090, 'exp': 1698673690
            }


class PhoneOtp(serializers.Serializer):
    phone_otp = serializers.CharField()
