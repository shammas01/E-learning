from django.shortcuts import render
from rest_framework.views import APIView
from . models import User,UserProfile
from . serializers import (
    Emailsmtpserializer,
    OtpSerializer,
    UserProfileSerializer,
    GoogleSocialAuthSerializer,
    PhoneOtpSerializer
    )
import math,random
from django.conf import settings
from useraccount.authentication.smtp import send_email
from useraccount.authentication.jwt import get_tokens_for_user
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import ( IsAuthenticated, )
from rest_framework.decorators import permission_classes
from useraccount.authentication.twilio import send_phone_sms,phone_otp_verify
from drf_spectacular.utils import extend_schema
# Create your views here.

class EmailOtpSendView(APIView):
    serializer_class=Emailsmtpserializer
    @extend_schema(responses=Emailsmtpserializer)
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
    serializer_class=OtpSerializer
    @extend_schema(responses=OtpSerializer)
    def post(self,requset):
        serializer = OtpSerializer(data=requset.data)
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


@permission_classes([IsAuthenticated])        
class UserProfileView(APIView):

    serializer_class=UserProfileSerializer
    @extend_schema(responses=UserProfileSerializer)

    def get(self,request):
        user = UserProfile.objects.get(user=request.user)# we can create with 'get_or_create()' method. 
        serializer = UserProfileSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request):
        user_profile = request.user.userprofile
        serializer=UserProfileSerializer(user_profile,data=request.data,partial=True)
        email = request.data.get('user', {}).get('email')
        print(request.data)
        user_email = request.user.email
        print(user_email)
        if serializer.is_valid():
            if email and email != user_email:
                otp = math.floor((random.randint(100000,999999)))
                subject = 'Otp for account verification'
                message = f'Your otp for account verification {otp}'
                recipient_list = [email]
                send_email(subject=subject, message=message, email=recipient_list[0])
                request.session['email'] = email
                request.session['otp'] = otp
                
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class EmailUpdatdOtpView(APIView):

    serializer_class=OtpSerializer
    @extend_schema(responses=OtpSerializer)

    def post(self, request):
        serialize =  OtpSerializer(data=request.data)
        if serialize.is_valid():
            otp = serialize.validated_data.get('otp')
            saved_otp = request.session.get('otp')
            email =  request.session.get('email')
            if otp == saved_otp:
                user = request.user
                user.email = email
                user.save()
                return Response("Email update successfully")
            else:
                return Response({"messege":"Invalid otp"})
        return Response(serialize.error_messages,status=status.HTTP_400_BAD_REQUEST)
    


class GoogleSocialAuthView(APIView):
    serializer_class=GoogleSocialAuthSerializer
    @extend_schema(responses=GoogleSocialAuthSerializer)
    def post(self,request):
        serializer = GoogleSocialAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])       
        return Response(data,status=status.HTTP_200_OK)



@permission_classes([IsAuthenticated])
class VerifyMobileNumber(APIView):
    serializer_class=PhoneOtpSerializer
    @extend_schema(responses=PhoneOtpSerializer)
    def post(self, request):
        serializer = PhoneOtpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone = serializer.validated_data.get('phone_number')
            request.session['phone_number'] = phone
            print(phone)
            try:
                verification_sid = send_phone_sms(phone)
                print(verification_sid)
                request.session['verification_sid'] = verification_sid
                return Response({"sid":verification_sid},status=status.HTTP_201_CREATED)
            except Exception as e:
                print(e)
            return Response({'msg':'somthing wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class PhoneOtpVerificationView(APIView):
    serializer_class=OtpSerializer
    @extend_schema(responses=OtpSerializer)
    def post(self, request):
        serializer = OtpSerializer(data=request.data)  
        if serializer.is_valid():
            otp = serializer.validated_data.get('otp')
            verification_sid = request.session.get('verification_sid')
            try:
                verification_check = phone_otp_verify(verification_sid, otp)
                print(verification_check.status) 
            except:
                return Response({'msg':'Something Went Wrong...'})
            if verification_check.status == 'approved':
                entered_phone_number=request.session.get('phone_number')
                user_profile = UserProfile.objects.get(user=request.user)
                user_profile.phone = entered_phone_number
                user_profile.save()
                response_data = {
                    "msg":"your phone number is verifyed",
                }                                               
                return Response(response_data)
            return Response({'msg': 'Something Went Wrong...'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

