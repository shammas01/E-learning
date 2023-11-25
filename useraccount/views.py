from django.shortcuts import render
from rest_framework.views import APIView
from .models import User, UserProfile
from .serializers import (
    Emailsmtpserializer,
    OtpSerializer,
    UserProfileSerializer,
    GoogleSocialAuthSerializer,
    PhoneOtpSerializer,
)
import math, random
from django.conf import settings
from useraccount.authentication.smtp import send_email
from useraccount.authentication.jwt import get_tokens_for_user
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.decorators import permission_classes
from useraccount.authentication.twilio import send_phone_sms, phone_otp_verify
from drf_spectacular.utils import extend_schema


# Create your views here.


class EmailOtpSendView(APIView):
    
    serializer_class = Emailsmtpserializer
    @extend_schema(responses=Emailsmtpserializer)
    def post(self, request):
        serializer = Emailsmtpserializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            otp = math.floor((random.randint(100000, 999999)))
            subject = "Otp for account verification"
            message = f"Your otp for account verification {otp}"
            # email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_email(subject=subject, message=message, email=recipient_list[0])
            request.session["email"] = email
            request.session["otp"] = otp
            return Response(
                {"email": email, "messegte": "email send successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailOtpVerifyView(APIView):
    
    serializer_class = OtpSerializer
    @extend_schema(responses=OtpSerializer)
    def post(self, requset):
        serializer = OtpSerializer(data=requset.data)
        if serializer.is_valid():
            otp = serializer.validated_data.get("otp")
            email = requset.session.get("email")
            saved_otp = requset.session.get("otp")
            if otp == saved_otp:
                user = User.objects.get_or_create(email=email)
                token = get_tokens_for_user(user[0])
                response = {
                    "token": token,
                    "messege": "your account successfull activated",
                }
                return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoogleSocialAuthView(APIView):

    serializer_class = GoogleSocialAuthSerializer
    @extend_schema(responses=GoogleSocialAuthSerializer)
    def post(self, request):
        serializer = GoogleSocialAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = (serializer.validated_data)["auth_token"]
        return Response(data, status=status.HTTP_200_OK)



