from django.shortcuts import render
from rest_framework.views import APIView
from . models import User,UserProfile
from . serializers import Emailsmtpserializer,EmailOtpSerializer,UserProfileSerializer,GoogleSocialAuthSerializer
import math,random
from django.conf import settings
from useraccount.authentication.smtp import send_email
from useraccount.authentication.jwt import get_tokens_for_user
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class EmailOtpSendView(APIView):
    def post(self,request):
        serializer = Emailsmtpserializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            otp = math.floor((random.randint(100000,999999)))
            subject = 'Otp for account verification'
            message = f'Your otp for account verification {otp}'
            # email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_email(subject=subject, message=message, email=recipient_list[0])
            request.session['email'] = email
            request.session['otp'] = otp
            return Response({"email":email,"messegte":"email send successfully"},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    


class EmailOtpVerifyView(APIView):
    def post(self,requset):
        serializer = EmailOtpSerializer(data=requset.data)
        if serializer.is_valid():
            otp= serializer.validated_data.get('otp')
            email = requset.session.get('email')
            saved_otp = requset.session.get('otp')
            if otp == saved_otp:
                user = User.objects.get_or_create(email=email)
                token = get_tokens_for_user(user[0])
                response = {"token":token,"messege":"your account successfull activated"}
                return Response(response,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        


class UserProfileView(APIView):
    def get(self,request):
        user = UserProfile.objects.get(user=request.user)# we can create with 'get_or_create()' method. 
        serializer = UserProfileSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)


    def put(self,request):
        user = request.user.userprofile
        serializer=UserProfileSerializer(user,data=request.data,partial=True)
        if serializer.is_valid():   
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

class GoogleSocialAuthView(APIView):
    
    def post(self,request):
        serializer = GoogleSocialAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data,status=status.HTTP_200_OK)