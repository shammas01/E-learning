from rest_framework.views import APIView
from .models import User
from .serializers import (
    Emailsmtpserializer,
    OtpSerializer,
    GoogleSocialAuthSerializer,


    UserRegisterSerializer
)
import math, random
from useraccount.authentication.smtp import send_email
from useraccount.authentication.jwt import get_tokens_for_user
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate

# Create your views here.


class RegisterEmailSendView(APIView):
    permission_classes_classes = [AllowAny]
    serializer_class = UserRegisterSerializer
    @extend_schema(responses=UserRegisterSerializer)
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get('password')
            

            User.objects.create_user(
                email = email,
                password = password,
            )

            otp = math.floor((random.randint(100000, 999999)))
            print(otp)
            subject = "Otp for account verification"
            message = f"Your otp for account verification {otp}"
            # email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_email(subject=subject, message=message, email=recipient_list[0])
            request.session["email"] = email
            request.session["otp"] = otp
            request.session['password'] = password
            return Response(
                {"email": email, "messegte": "email send successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class loginView(APIView):
    serializer_class = OtpSerializer
    @extend_schema(responses=OtpSerializer)
    def post(self, requset):
        serializer = OtpSerializer(data=requset.data)
    
        if serializer.is_valid():
            otp = serializer.validated_data.get("otp")
            password = serializer.validated_data.get('password')
            email = requset.session.get("email")
            saved_otp = requset.session.get("otp")
            saved_password = requset.session.get('password')

            
            if otp == saved_otp and password == saved_password:
                user = User.objects.get(email=email)
                token = get_tokens_for_user(user)
                response = {
                    "Your email": email,
                    "token": token,
                    "messege": "your account successfull activated",
                }
                return Response(response, status=status.HTTP_200_OK)
            return Response("somthing wrong....!")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoogleSocialAuthView(APIView):

    serializer_class = GoogleSocialAuthSerializer
    @extend_schema(responses=GoogleSocialAuthSerializer)
    def post(self, request):
        serializer = GoogleSocialAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = (serializer.validated_data)["auth_token"]
        return Response(data, status=status.HTTP_200_OK)



